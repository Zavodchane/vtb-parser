from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import time


def find_element(driver: webdriver.Chrome, by: By, value: str, attribute: str, name: str):
    for element in driver.find_elements(by=by, value=value):
        if element.get_attribute(attribute) is None:
            continue

        if name in element.get_attribute(attribute):
            return element
    return None


def find_elements(driver: webdriver.Chrome, by: By, value: str, attribute: str, name: str):
    _l: list = []
    for element in driver.find_elements(by=by, value=value):
        if element.get_attribute(attribute) is None:
            continue

        if name in element.get_attribute(attribute):
            _l.append(element)
    return _l


def click_to_element(driver: webdriver.Chrome, element):
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable(element))
    driver.execute_script('arguments[0].click()', element)
    time.sleep(0.3)
