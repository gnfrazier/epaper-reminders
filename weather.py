
#%%writefile "/home/greg/Documents/python/notebooks/epaper/weather.py"


import time
import arrow as arw
import json

import requests

with open('conditions_key.json','r') as file:
    
    condition_keys = json.load(file)

    
    
def to_f(celsius):
    
    if celsius:
        f = int((float(celsius) * 1.8) + 32)
    else:
        f = None
        
    return f

def to_mph(kmh):
    
    if kmh:
        mph = int(float(kmh) / 1.609)
    
    return mph
    
def get_json(url, seconds=10):
    
    response = requests.get(url).json()
    
    if response.get('status') == 503:
        
        print('Service did not respond, waiting {seconds} to retry')
        time.sleep(seconds)
        seconds = seconds + 60
        response = get_json(url, seconds)
        
    return response

def get_nearest_station(station_url):
    stations = get_json(station_url)

    identifier = stations['features'][0]['properties']['stationIdentifier']

    return identifier

def parse_hourly(hourly):
    
    parsed = {}
    
    
    for period in hourly['properties']['periods']:
        position = period['number']
        day = arw.get(period['startTime']).format("DD")
        hour = arw.get(period['startTime']).format("HH")
        temperature = period['temperature']
        wind = period['windSpeed'].replace(' mph','')
        wind_dir = period['windDirection']
        conditions_icon, precip = url_to_icon_precip(period['icon'])
        
        
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


def get_hourly(station_info=None):
    
    
    if station_info != True:
        station_info = get_json(noaa_api)
    hourly_url = station_info['properties']['forecastHourly']
    
    hourly = get_json(hourly_url)
    formatted_hourly = parse_hourly(hourly)
        
    return formatted_hourly

def get_current(station_info=None):
    
    
    if station_info !=True:
        station_info = get_json(noaa_api)

    stations_url = station_info['properties']['observationStations']
    station_id = get_nearest_station(stations_url)
    nearest_conditions_url = 'https://api.weather.gov/stations/{}/observations'.format(station_id)
    current_cond = get_json(nearest_conditions_url)
    
    formatted_current = parse_current(current_cond)
 
    return formatted_current
  
def parse_current(present_conditions):
    latest = present_conditions['features'][0]['properties'] 

    present_weather = {
            'cur_timestamp':latest['timestamp'],
            'cur_temp':to_f(latest['temperature']['value']),
            'cur_wind':to_mph(latest['windSpeed']['value']),
            'cur_wind_dir':latest['windDirection']['value'],
            'cur_humidity':int(latest['relativeHumidity']['value']),
            'cur_heat_index':to_f(latest['heatIndex']['value']),
            'cur_wind_chill':to_f(latest['windChill']['value']),
                }
    return present_weather
 

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
        grid_data_url = station_info['properties']['forecastGridData']
        stations_url = station_info['properties']['observationStations']
        city_state = station_info['properties']['relativeLocation']['properties']

        station_id = get_nearest_station(stations_url)
        nearest_conditions_url = 'https://api.weather.gov/stations/{}/observations'.format(station_id)
        current_cond = get_json(nearest_conditions_url)

        hourly = get_json(hourly_url)
        formatted_hourly = parse_hourly(hourly)
    else:
        print('Unable to reach weather.gov please wait and try again.')
  
