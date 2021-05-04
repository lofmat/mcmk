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
td_mand_fields_only = {'name': 'New one 1111111111111111111111', 'price': '11111111111'}
# td_full = {'name': 'To be updated 1', 'price': 900, 'street': 'Street 2', 'rooms': 3, 'status': 'true'}
# td_empty = {'name': '', 'price': '', 'street': '', 'rooms': '', 'status': ''}


@pytest.mark.skip
@pytest.mark.parametrize("data", [td_mand_fields_only])
def test_update_existing_ad(data):
    # Create ad
    response = requests.post(url, json=data)
    rd = response.json()
    tmp_json = rd.copy()
    tmp_json.pop('_id', None)
    assert sorted(data.items()) == sorted(tmp_json.items()), 'POST request failed'
    # Change ad
    updated_data = {'name': f"Updated {data['name']}", 'price': "1", '_id': f"{rd['_id']}"}
    r = requests.put(f"{url}/{rd['_id']}", json=updated_data)
    # Updated 1 item
    assert int(r.text) == 1, 'Must be updated only 1 item'
    upd_r = requests.get(f"{url}/{rd['_id']}")
    assert sorted(upd_r.json().items()) == sorted(updated_data.items()), f'Prepared data {updated_data} ' \
                                                                         f'different with requested {upd_r}'

@pytest.mark.skip
def test_update_non_existent_ad():
    fake_id = '0000000000000000'
    # Change fake ad
    data = {'name': f"{fake_id}", 'price': "1", '_id': fake_id}
    r = requests.put(f"{url}/{fake_id}", json=data)
    assert int(r.text) == 0, 'It should not be updated any entries'


@pytest.mark.skip
@pytest.mark.parametrize("data", [td_mand_fields_only])
def test_update_existing_ad_with_the_same_data(data):
    # Create ad
    response = requests.post(url, json=data)
    rd = response.json()
    tmp_json = rd.copy()
    tmp_json.pop('_id', None)
    assert sorted(data.items()) == sorted(tmp_json.items()), 'POST request failed'
    # Change ad
    r = requests.put(f"{url}/{rd['_id']}", json=data)
    # Updated 1 item
    assert int(r.text) == 1, 'Must be updated only 1 item'
    upd_r = requests.get(f"{url}/{rd['_id']}")
    assert sorted(data.items()) == sorted(upd_r.json().items()), 'PUT request failed'


@pytest.mark.skip
@pytest.mark.parametrize("data", [td_mand_fields_only])
def test_update_existing_post_with_too_long_name(data):
    # Create ad
    response = requests.post(url, json=data)
    rd = response.json()
    tmp_json = rd.copy()
    tmp_json.pop('_id', None)
    assert sorted(data.items()) == sorted(tmp_json.items()), 'POST request failed'
    # Change ad
    updated_data = {'name': "0" * 100, 'price': "1", '_id': f"{rd['_id']}"}
    r = requests.put(f"{url}/{rd['_id']}", json=updated_data)
    # Updated 1 item
    assert int(r.text) == 1, 'Must be updated only 1 item'
    upd_r = requests.get(f"{url}/{rd['_id']}")
    # TODO What is expected behavior? Max length is 50???
    assert sorted(upd_r.json().items()) == sorted(updated_data.items()), f'Prepared data {updated_data} ' \
                                                                         f'different with requested {upd_r}'


@pytest.mark.skip
@pytest.mark.parametrize("data", [td_mand_fields_only])
def test_update_existing_post_with_non_existent_field(data):
    # Create ad
    response = requests.post(url, json=data)
    rd = response.json()
    tmp_json = rd.copy()
    tmp_json.pop('_id', None)
    assert sorted(data.items()) == sorted(tmp_json.items()), 'POST request failed'
    # Change ad
    updated_data = {'name': "Name", 'price': "1", '_id': f"{rd['_id']}", 'additional_field': 100}
    r = requests.put(f"{url}/{rd['_id']}", json=updated_data)
    # Updated 1 item
    # TODO what is expected behavior? I guess it isn't acceptable to allow to add new fields
    assert int(r.text) == 0, 'Must be updated only 0 item'


@pytest.mark.parametrize("data", [{'name': "SuperXXX12eqweqew2 nameXXX12", 'price': "999923299"}])
def test_update_existing_post_with_non_existent_field(data):
    # Create ad
    response = requests.post(url, json=data)
    rd = response.json()
    tmp_json = rd.copy()
    tmp_json.pop('_id', None)
    # assert sorted(data.items()) == sorted(tmp_json.items()), 'POST request failed'

    k = requests.put(f"{url}/{rd['_id']}", json={})
                         #, json={"name": "Super name", "price": "999999", "_id": 'zKN5bYtr5dgBZYCI'})
    print('111 ', k.text)
    hh = requests.patch(f"{url}/{rd['_id']}", json={'name':'1111111100000000001111111111'})
    print('000', hh.text)
    jj = requests.delete(f"{url}/{rd['_id']}")
    print('1,4', jj.text)
    knx = requests.get(f"{url}/{rd['_id']}")
    print('222', knx.text)
    assert knx