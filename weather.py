

import time
import arrow as arw
import json

import requests

with open('conditions_key.json','r') as file:
    
    condition_keys = json.load(file)

    
def get_json(url, seconds=10):
    
    response = requests.get(url).json()
    
    if response.get('status') == 503:
        
        print('Service did not respond, waiting {seconds} to retry')
        time.sleep(seconds)
        seconds = seconds + 60
        response = get_json(url, seconds)
        
    return 


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
        conditions_icon, precip = url_to_icon_precip(period['icon'])
        
        print('Day: {}  Hour: {}  Temp: {}  Wind: {} Icon: {} Precip %: {}'.format(
                            day, hour, temperature, wind, conditions_icon, precip))
        
        parsed[position] = {'position':position,
                           'day':day,
                           'hour':hour,
                           'temp':temperature,
                           'wind':wind,
                           'wind_dir':wind_dir,
                           'conditions_icon':conditions_icon,
                            'precip_percent':precip,
                           
                           }
        
    return parsed


def get_hourly():
    
    noaa_api = "https://api.weather.gov/points/" + lat_long
    
    station_info = get_json(noaa_api)
    hourly_url = station_info['properties']['forecastHourly']
    
    hourly = get_json(hourly_url)
    formatted_hourly = parse_hourly(hourly)
        
    return formatted_hourly


def url_to_icon_precip(url):
   # Parse the URL to the conditions short code
    condition_short_code_with_precip = url.split('/')[-1].split('?')[0]
    
    condition_short_code = condition_short_code_with_precip.split(',')[0]
    
    # Precip percentage is after a comma, but not always
    try:
        precip = condition_short_code_with_precip.split(',')[1]
        
    except:
        precip = " "
       
    return (condition_keys['icons'][condition_short_code]['icon'], precip)


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
    
