import os

import configparser
import logging
import requests
import pytest

# Extended interpolation allows read section inside ini config
config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())

# Read test configuration file
cfg_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config', 'test.ini')
logging.info(f'Using config -> {cfg_path}')
config.read(cfg_path)
if config.has_section('TEST_CONFIG') and config['TEST_CONFIG'].get('api_endpoint'):
    url = config['TEST_CONFIG']['api_endpoint']
else:
    raise ValueError(f"No 'TEST_CONFIG' section of 'api_endpoint' in config {cfg_path}.")

# test data
# CORRECT PARAMS
td_mand_fields_only = {'name': 'Apartments in Kreuzeberg', 'price': '900'}
td_full = {'name': 'Apt1', 'price': 900, 'street': 'Unter den Linden', 'rooms': 3, 'status': 'true'}
td_empty = {'name': '', 'price': '', 'street': '', 'rooms': '', 'status': ''}
td_several_items = {'name': ['Apt1', 'Apt2', 'Apt3'],
                    'price': [1, 2, 3],
                    'street': ['Str1', 'Str2', 'Str3'],
                    'rooms': [1, 2, 3],
                    'status': ['false', 'true', '']}

# ---- TODO Review cases ----
# INCORRECT PARAMS
# Wrong value of parameters
td_wrong_price_val = {'name': 'Apt 1', 'price': 'false', 'street': 'Street1', 'rooms': 3, 'status': 'true'}
td_wrong_name_val = {'name': 'false', 'price': 900, 'street': 'Street1', 'rooms': 3, 'status': 'true'}
td_wrong_street_val = {'name': 'Apt2', 'price': 1000, 'street': -1, 'rooms': 3, 'status': 'true'}
td_wrong_rooms_val = {'name': 'Apt3', 'price': 1000, 'street': 'Street2', 'rooms': -1, 'status': 'true'}
td_wrong_status_val = {'name': 'Apt4', 'price': 1000, 'street': 'Street3', 'rooms': 4, 'status': 4}

# Injections
td_injection_name = {'name': "'; select true; --", 'price': 900, 'street': 'Linden', 'rooms': 3, 'status': 'true'}
td_injection_price = {'name': "Apt2", 'price': "'; select true; --", 'street': 'Linden', 'rooms': 3, 'status': 'true'}
td_injection_street = {'name': "Apt3", 'price': 900, 'street': "'; select true; --", 'rooms': 3, 'status': 'true'}
td_injection_rooms = {'name': "Apt4", 'price': 900, 'street': "Linden", 'rooms': "'; select true; --", 'status': 'true'}
td_injection_status = {'name': "Apt5", 'price': 900, 'street': "Linden", 'rooms': 3, 'status': "'; select true; --"}

# Overflow
td_overflow_name = {'name': 'a' * 100, 'price': 900, 'street': 'Linden', 'rooms': 3, 'status': 'true'}

# Localization
td_german_symbols = {'name': 'Ö' * 10, 'price': 900, 'street': 'Linden', 'rooms': 3, 'status': 'true'}


@pytest.mark.parametrize("data", [td_mand_fields_only, td_full, td_empty])
def test_create_new_ad_correct_params(data):
    response = requests.post(url, json=data)
    rd = response.json()
    assert '_id' in rd.keys()
    rd.pop('_id', None)
    assert sorted(data.items()) == sorted(rd.items()), "Request's payload and returned json are different"


@pytest.mark.parametrize("data", [td_several_items])
def test_create_several_new_ad(data):
    res = 0
    for i in range(3):
        dt = {'name': data['name'][i],
              'price': data['price'][i],
              'street': data['street'][i],
              'rooms': data['rooms'][i],
              'status': data['status'][i]}
        response = requests.post(url, json=dt)
        assert response.status_code == requests.codes.ok
        for k in requests.get(url).json():
            k.pop('_id', None)
            if sorted(dt.items()) == sorted(k.items()):
                res = 1
                break
        assert res == 1


@pytest.mark.parametrize("data", [td_wrong_name_val, td_wrong_street_val, td_wrong_price_val,
                                  td_wrong_rooms_val, td_wrong_status_val])
def test_create_new_ad_wrong_params(data):
    response = requests.post(url, json=data)
    rd = response.json()
    assert '_id' in rd.keys()
    rd.pop('_id', None)
    assert response.status_code != requests.codes.ok
    assert sorted(data.items()) != sorted(rd.items())


@pytest.mark.parametrize("data", [td_injection_name, td_injection_price, td_injection_rooms,
                                  td_injection_status, td_injection_street])
def test_create_new_ad_injections(data):
    response = requests.post(url, json=data)
    rd = response.json()
    # Also should be some error message
    assert response.status_code != requests.codes.ok, 'The field may be subject to injection'
    assert sorted(data.items()) != sorted(rd.items()), 'No error message! Returned the same json.'


@pytest.mark.parametrize("data", [td_overflow_name])
def test_create_new_ad_injections(data):
    response = requests.post(url, json=data)
    rd = response.json()
    # Also should be some error message
    assert response.status_code != requests.codes.ok, 'The field can only be 50 characters long'
    assert sorted(data.items()) != sorted(rd.items()), 'No error message! Returned the same json.'


@pytest.mark.parametrize("data", [td_german_symbols])
def test_create_new_ad_injections(data):
    response = requests.post(url, json=data)
    rd = response.json()
    assert '_id' in rd.keys()
    rd.pop('_id', None)
    assert sorted(data.items()) == sorted(rd.items()), "Request's payload and returned json are different"


