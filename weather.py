

import time
import arrow as arw

import requests

def get_json(url, seconds=10):
    
    response = requests.get(url).json()
    
    if response.get('status') == 503:
        
        print('Service did not respond, waiting {seconds} to retry')
        time.sleep(seconds)
        seconds = seconds + 60
        response = get_json(url, seconds)
        
    return response
def parse_hourly(hourly):
    
    parsed = {}
    
    # TODO Extract percent chance of rain
    for period in hourly['properties']['periods']:
        position = period['number']
        day = arw.get(period['startTime']).format("DD")
        hour = arw.get(period['startTime']).format("HH")
        temperature = period['temperature']
        wind = period['windSpeed'].replace(' mph','')
        wind_dir = period['windDirection']
        print('Day: {}  Hour: {}  Temp: {}  Wind: {}'.format(day, hour, temperature, wind))
        
        parsed[position] = {'position':position,
                           'day':day,
                           'hour':hour,
                           'temp':temperature,
                           'wind':wind,
                           'wind_dir':wind_dir}
        
    return parsed

def get_hourly():
    
    noaa_api = "https://api.weather.gov/points/" + lat_long
    
    station_info = get_json(noaa_api)
    hourly_url = station_info['properties']['forecastHourly']
    
    hourly = get_json(hourly_url)
    formatted_hourly = parse_hourly(hourly)
        
    return formatted_hourly


# TODO - use config file
lat_long = "36.064444,-79.398056"

noaa_api = "https://api.weather.gov/points/" + lat_long

if __name__ == '__main__':

    station_info = get_json(noaa_api)
    if station_info:
        forecast_url = station_info['properties']['forecast']
        hourly_url = station_info['properties']['forecastHourly']
        stations_url = station_info['properties']['observationStations']
        city_state = station_info['properties']['relativeLocation']['properties']

        hourly = get_json(hourly_url)
        formatted_hourly = parse_hourly(hourly)
    else:
        print('Unable to reach weather.gov please wait and try again.')
    
