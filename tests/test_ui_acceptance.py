#!/usr/bin/env python

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime
import configparser
import logging
import os
import pytest

# Extended interpolation allows read section inside ini config
config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())

# Read test configuration file
cfg_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config', 'test.ini')
logging.info(f'Using config -> {cfg_path}')
config.read(cfg_path)
selenium_driver_path = config['TEST_CONFIG']['selenium_driver_path']
test_url = config['TEST_CONFIG']['site_under_test']


@pytest.fixture()
def setup(request):
    print("initiating chrome driver")
    driver = webdriver.Firefox(selenium_driver_path)
    request.instance.driver = driver
    driver.get(test_url)
    driver.maximize_window()
    yield driver
    driver.close()


@pytest.mark.usefixtures("setup")
class TestExample:
    def test_simple_scenario(self):
        td = {'name': 'Name1', 'price': 1000, 'street': 'Street1', 'rooms': 1, 'status': 'Active'}
        self.driver.find_element_by_xpath("//span/a[@href='/advertisement/new']").click()
        # Fill name
        self.driver.find_element_by_xpath("//input[@id='input_0']").send_keys(td['name'])
        # Fill street
        self.driver.find_element_by_xpath("//*[@id='input_1']").send_keys(td['street'])
        # Fill rooms
        self.driver.find_element_by_xpath("//*[@id='input_2']").send_keys(td['rooms'])
        # Fill price
        self.driver.find_element_by_xpath("//*[@id='input_3']").send_keys(td['price'])
        # Fill status
        self.driver.find_element_by_xpath("//form/md-checkbox[@aria-label='Status']/div[1]").click()
        # Save changes
        self.driver.find_element_by_xpath("//div/button[2]/span[contains (text(), 'save')]").click()
        table = self.driver.find_element_by_xpath("//section/advertisement-list/div/div/md-table-container/table")
        lines = table.find_elements_by_tag_name('tr')
        m = False
        for ln in lines:
            line = ln.get_attribute("innerHTML")
            m = (str(td['name']) in line) and ('1.000,00' in line) and (str(td['street']) in line) and \
                (str(td['status']) in line) and (str(td['rooms']) in line)
            if m:
                break
        assert m
