import os
import json
import dotenv
import requests
import pandas as pd

dotenv.load_dotenv('.env')
TOKEN = os.environ.get('OPEN_WEATHER_TOKEN')
LOCATION = os.environ.get('LOCATION', 'Brooklyn')
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
KtoC = lambda kelvin: kelvin - 273.15

def extract():
    ''' Query the API and write out new data to JSONL '''
    # Query the current weather
    response = requests.get(BASE_URL, params={'q': LOCATION, 'appid': TOKEN})
    if response.ok:
        # Write out as line of JSONL
        with open('weather_kelvin.jsonl', 'a') as wfile:
            wfile.write( json.dumps(response.json()) + '\n' )
    else:
        raise ValueError(f'OpenWeather API returned {response.status_code}')

def transform():
    ''' Transform step: transform minimal useful data and convert kelvin->celsius '''
    raw_data = [json.loads(x) for x in open('weather_kelvin.jsonl').readlines()]
    transformed_data = [
        {
            'name':jdata['name'],
            'dt':jdata['dt'],
            **{key: KtoC(jdata['main'][key]) for key in ('temp', 'feels_like', 'temp_min', 'temp_max')}
        }
        for jdata in raw_data
    ]
    # Write out transformed_data
    pd.DataFrame(transformed_data).to_json('weather_celsius.jsonl', orient='records', lines=True)

def load():
    ''' Load step: Just print the DataFrame to the console '''
    df = pd.read_json('weather_celsius.jsonl', lines=True, convert_dates=['dt'], date_unit='s')
    print(df)

def main():
    extract()
    transform()
    load()

if __name__ == '__main__':
    main()