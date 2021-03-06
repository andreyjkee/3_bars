import json
import os
from math import sin, cos, sqrt, atan2, radians
from optparse import OptionParser


def load_data(filepath):
    if not filepath:
        raise Exception('Не указан путь к файлу')
    if not os.path.exists(filepath):
        raise Exception('Файл {0} не найден'.format(filepath))
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        return json.loads(f.read())

def get_biggest_bar(data):
    return max(data, key=lambda bar: bar['SeatsCount'] and bar['TypeObject'] == 'бар')


def get_smallest_bar(data):
    return min(data, key=lambda bar: bar['SeatsCount'] and bar['TypeObject'] == 'бар')


def get_closest_bar(data, latitude, longitude):
    return min(data, key=lambda bar: get_distance(latitude, longitude, bar['Latitude_WGS84'], bar['Longitude_WGS84']))

def get_distance(lat1, lon1, lat2, lon2):
    lat1_r = radians(float(lat1))
    lon1_r = radians(float(lon1))
    lat2_r = radians(float(lat2))
    lon2_r = radians(float(lon2))
    dlon = lon2_r - lon1_r
    dlat = lat2_r - lat1_r
    a = sin(dlat / 2) ** 2 + cos(lat1_r) * cos(lat2_r) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    earth_radius = 6373.0
    return earth_radius * c

def get_pretty_bar_name(bar):
    return 'Название: {0}, Мест: {1}'.format(bar['Name'], bar['SeatsCount'])

def is_correct_latitude(latitude):
    return -90 <= float(latitude) <= 90

def is_correct_longitude(longitude):
    return -180 <= float(longitude) <= 180


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-f', '--file', type='string', dest='filepath')
    options, args = parser.parse_args()
    json_content = load_data(options.filepath)
    print('Biggest bar: ', get_biggest_bar(json_content))
    print('Smallest bar: ', get_smallest_bar(json_content))
    print('Please input your latitude coordinate:')
    latitude = input()
    if not is_correct_latitude(latitude):
        raise Exception({'message': 'Incorrect latitude coordinate'})
    print('Please input your longitude coordinate:')
    longitude = input()
    if not is_correct_longitude(longitude):
        raise Exception({'message': 'Incorrect longitude coordinate'})
    print('Closest bar: ', get_closest_bar(json_content, latitude, longitude))
