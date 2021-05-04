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


td = {'name': 'Mitte Apartments', 'price': 900.0, 'street': 'Unter den Linden', 'rooms': 3, 'status': 'true'}


# PUT  method
@pytest.mark.parametrize("data", [td])
def test_update_existing_ad(data):
    # Create ad
    post_resp = requests.post(url, json=data).json()
    tmp_json = post_resp.copy()
    tmp_json.pop('_id', None)
    # Check value that post returned
    assert sorted(data.items()) == sorted(tmp_json.items()), 'POST request failed'
    get_resp = requests.get(f"{url}/{post_resp['_id']}").json()
    # Check that ad exist
    assert sorted(get_resp.items()) == sorted(post_resp.items()), 'POST request failed'
    # Change ad
    updated_data = {'name': f"Updated {data['name']}",
                    'price': {int(data['price']) + 1000},
                    'street': f"Updated {data['street']}",
                    'rooms': {int(data['rooms']) + 3},
                    'status': 'false',
                    '_id': f"{post_resp['_id']}"}
    r = requests.put(f"{url}/{post_resp['_id']}", json=updated_data)
    # Updated 1 item
    assert int(r.text) == 1, 'Must be updated only 1 item'
    upd_r = requests.get(f"{url}/{post_resp['_id']}")
    assert sorted(upd_r.json().items()) == sorted(updated_data.items()), f'Prepared data {updated_data} ' \
                                                                         f'different with requested {upd_r}'


def test_update_non_existent_ad():
    fake_id = '0000000000000000'
    # Change fake ad
    data = {'name': f"{fake_id}", 'price': "1", '_id': fake_id}
    r = requests.put(f"{url}/{fake_id}", json=data)
    assert int(r.text) == 0, 'It should not be updated any entries'


@pytest.mark.parametrize("data", [td])
def test_update_existing_ad_with_the_same_data(data):
    # Create ad
    response = requests.post(url, json=data)
    rd = response.json()
    tmp_json_post = rd.copy()
    tmp_json_post.pop('_id', None)
    assert sorted(data.items()) == sorted(tmp_json_post.items()), 'POST request failed'
    # Change ad
    r = requests.put(f"{url}/{rd['_id']}", json=data)
    # Updated 1 item
    assert int(r.text) == 1, 'Must be updated only 1 item'
    upd_r = requests.get(f"{url}/{rd['_id']}")
    tmp_json_get = upd_r.json()
    tmp_json_get.pop('_id', None)
    assert sorted(data.items()) == sorted(tmp_json_get.items()), 'PUT request failed'


# "PATCH  method"
@pytest.mark.parametrize("data", [td])
def test_update_existing_ad(data):
    # Create ad
    post_resp = requests.post(url, json=data).json()
    tmp_json = post_resp.copy()
    tmp_json.pop('_id', None)
    # Check value that post returned
    assert sorted(data.items()) == sorted(tmp_json.items()), 'POST request failed'
    get_resp = requests.get(f"{url}/{post_resp['_id']}").json()
    # Check that ad exist
    assert sorted(get_resp.items()) == sorted(post_resp.items()), 'POST request failed'
    # Partial update
    updated_data = {'name': f"Updated {data['name']}",
                    'price': data['price'],
                    'street': data['street'],
                    'rooms': data['rooms'],
                    'status': 'false',
                    '_id': f"{post_resp['_id']}"}
    r = requests.put(f"{url}/{post_resp['_id']}", json=updated_data)
    # Updated 1 item
    assert int(r.text) == 1, 'Must be updated only 1 item'
    upd_r = requests.get(f"{url}/{post_resp['_id']}")
    assert sorted(upd_r.json().items()) == sorted(updated_data.items()), f'Prepared data {updated_data} ' \
                                                                         f'different with requested {upd_r}'


@pytest.mark.parametrize("data", [td])
def test_update_existing_post_with_too_long_name(data):
    # Create ad
    response = requests.post(url, json=data)
    rd = response.json()
    tmp_json = rd.copy()
    tmp_json.pop('_id', None)
    assert sorted(data.items()) == sorted(tmp_json.items()), 'POST request failed'
    # Change ad
    updated_data = {'name': "0" * 100,
                    'price': data['price'],
                    'street': data['street'],
                    'rooms': data['rooms'],
                    'status': 'false',
                    '_id': f"{rd['_id']}"}
    r = requests.put(f"{url}/{rd['_id']}", json=updated_data)
    # Updated 1 item
    assert int(r.text) == 1, 'Must be updated only 1 item'
    upd_r = requests.get(f"{url}/{rd['_id']}")
    # TODO What is expected behavior? Max length is 50???
    assert sorted(upd_r.json().items()) == sorted(updated_data.items()), f'Prepared data {updated_data} ' \
                                                                         f'different with requested {upd_r}'


@pytest.mark.parametrize("data", [td])
def test_update_existing_post_with_non_existent_field(data):
    # Create ad
    response = requests.post(url, json=data)
    rd = response.json()
    tmp_json = rd.copy()
    tmp_json.pop('_id', None)
    assert sorted(data.items()) == sorted(tmp_json.items()), 'POST request failed'
    # Change ad
    updated_data = {'name': 'Name',
                    'price': data['price'],
                    'street': data['street'],
                    'rooms': data['rooms'],
                    'status': 'false',
                    '_id': f"{rd['_id']}",
                    'additional_field': 100}
    r = requests.put(f"{url}/{rd['_id']}", json=updated_data)
    # Updated 1 item
    # TODO what is expected behavior? I guess it isn't acceptable to allow to add new fields
    assert int(r.text) == 0, 'Should be returned error instead of updated entries number'
