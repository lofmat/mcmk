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


# TODO check DELETE method implementation to make cleanup before/after tests
# Check connection before test suite
@pytest.fixture(scope="session", autouse=True)
def check_connection_before_suite():
    # Code that will run before your test suite
    r = requests.get(url)
    if r.status_code != 200:
        raise Exception(f"Test endpoint cannot be reached. \n "
                        f"HTTP status code -> {r.status_code}. \n "
                        f"Please check test config -> {cfg_path}")
    yield


# TODO move test data to separate class
# Test data
correct_params = [
    # ----------- Price --------------
    {'name': 'A1', 'price': 12.12, 'street': 'S1', 'rooms': 3, 'status': 'true'},
    {'name': 'A1', 'price': '12,12', 'street': 'S1', 'rooms': 3, 'status': 'true'},
    {'name': 'A1', 'price': '122.122,12', 'street': 'S1', 'rooms': 3, 'status': 'true'},
    # ----------- Name --------------
    {'name': 'n' * 50, 'price': 900, 'street': 'S1', 'rooms': 3, 'status': 'true'},
    {'name': 'n' * 49, 'price': 900, 'street': 'S1', 'rooms': 3, 'status': 'false'},
    {'name': 'Wohnung Mitte Klein', 'price': 900, 'street': 'S1', 'rooms': 1, 'status': 'false'},
    {'name': 'WÖhnung', 'price': 900, 'street': 'S1', 'rooms': 1, 'status': 'false'},
    # ----------- Street --------------
    {'name': 'A1', 'price': 900, 'street': 'Wilhelmstraße 34', 'rooms': 1, 'status': 'false'},
    {'name': 'A1', 'price': 900, 'street': '', 'rooms': 1, 'status': 'false'},
    # ----------- Rooms ---------------
    {'name': 'A1', 'price': 12.12, 'street': 'S1', 'rooms': '3' * 10000, 'status': 'true'},
    {'name': 'A1', 'price': 12.12, 'street': 'S1', 'rooms': '', 'status': 'true'},
]

# Backend should reject the following requests
incorrect_params = [
    # ----------- Name --------------
    {'name': 'n' * 51, 'price': 900, 'street': 'S1', 'rooms': 3, 'status': 'true'},
    {'name': "'; select true; --", 'price': 900, 'street': 'S1', 'rooms': 3, 'status': 'true'},
    {'name': '', 'price': 900, 'street': 'S1', 'rooms': 3, 'status': 'true'},
    # ----------- Price -------------
    {'name': 'A1', 'price': "122'; select true; --", 'street': 'S1', 'rooms': 3, 'status': 'true'},
    {'name': 'A1', 'price': 'false', 'street': 'S1', 'rooms': 3, 'status': 'true'},
    {'name': 'A1', 'price': '', 'street': 'S1', 'rooms': 3, 'status': 'true'},
    {'name': 'A1', 'price': '3' * 10000, 'street': 'S1', 'rooms': 3, 'status': 'true'},
    # ----------- Street ------------
    {'name': 'A1', 'price': 900, 'street': -1, 'rooms': 1, 'status': 'false'},
    {'name': 'A1', 'price': 900, 'street': "'; select true; --", 'rooms': 1, 'status': 'false'},
    # ----------- Rooms -------------
    {'name': 'A1', 'price': 12.12, 'street': 'S1', 'rooms': -1, 'status': 'true'},
    {'name': 'A1', 'price': 12.12, 'street': 'S1', 'rooms': "'; select true; --", 'status': 'true'},
    # ----------- Status ------------
    {'name': 'A1', 'price': 12.12, 'street': 'S1', 'rooms': 1, 'status': ''},
    {'name': 'A1', 'price': 12.12, 'street': 'S1', 'rooms': 1, 'status': 1},
    {'name': 'A1', 'price': 12.12, 'street': 'S1', 'rooms': 1, 'status': "'; select true; --"},
]


# Positive tests
@pytest.mark.parametrize("data", correct_params)
def test_create_new_ad_correct_params(data):
    post_resp = requests.post(url, json=data).json()
    assert '_id' in post_resp.keys()
    item_id = post_resp['_id']
    tmp = post_resp.copy()
    tmp.pop('_id', None)
    assert sorted(data.items()) == sorted(tmp.items()), "Request's payload and returned json are different"
    get_resp = requests.get(f'{url}/{item_id}').json()
    assert sorted(post_resp.items()) == sorted(get_resp.items()), "Request's payload and returned json are different"


# Negative tests
@pytest.mark.parametrize("data", incorrect_params)
def test_create_new_ad_incorrect_params(data):
    response = requests.post(url, json=data)
    rd = response.json()
    assert '_id' in rd.keys()
    rd.pop('_id', None)
    # Depends on backend implementation
    # I guess that server must return some error code
    assert response.status_code != requests.codes.ok
    assert sorted(data.items()) != sorted(rd.items())

