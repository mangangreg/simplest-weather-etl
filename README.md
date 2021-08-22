# etl-simplestweather
The simplest single-file python ETL pipeline, all contained in [etl.py](./etl.py).

## Setup
### OpenWeather
This app uses the OpenWeatherMap API, so to use this code you need a (free) account on [OpenWeatherMap.org](OpenWeatherMap.org), to get an API access token.

## env file
This app expects a `.env` file with the following environment variables defined:
- OPEN_WEATHER_TOKEN: API access token from OpenWeatherMap
- LOCATION: Optional, location parameter for location to be queried for weather
