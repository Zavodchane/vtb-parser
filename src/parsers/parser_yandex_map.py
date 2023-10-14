from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from src.parsers.browser import find_element, find_elements, click_to_element
from src.timers.timers import timer

import time


chrome_options = Options()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--disable-web-security")
chrome_options.add_argument("--allow-running-insecure-content")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                          options=chrome_options)


def open_browser():
    driver.get("https://yandex.ru/maps/?ll=93.586454%2C41.303117&z=2")
    driver.maximize_window()
    time.sleep(4)


def input_address_in_search_window(address: str, sub: str = ""):
    inpt = find_element(driver=driver,
                        by=By.TAG_NAME, value="input", attribute="class", name="input__control _bold")
    inpt.send_keys(f"{sub} {address}")
    inpt.send_keys(Keys.ENTER)
    time.sleep(5)


def get_rating() -> float:
    rating = driver.find_element(by=By.CLASS_NAME, value="business-rating-badge-view__rating-text._size_m")
    return float(rating.text.replace(",", "."))


def get_possibilities() -> list:
    try:
        features = driver.find_element(by=By.CLASS_NAME, value="tabs-select-view__title._name_features")
    except:
        click_to_first_search_tab()
        features = driver.find_element(by=By.CLASS_NAME, value="tabs-select-view__title._name_features")
    click_to_element(driver, features)
    time.sleep(4)
    possibilities_web = driver.find_elements(by=By.CLASS_NAME, value="business-features-view__bool-text")
    return list(map(lambda x: x.text, possibilities_web))


def get_permitted_operation():
    permitted_operation = driver.find_elements(by=By.CLASS_NAME, value="business-features-view__valued-value")[5]
    return permitted_operation.text


def is_work_office() -> bool:
    try:
        driver.find_element(by=By.CLASS_NAME, value="business-working-status-view._closed._no-data")
        return False
    except:
        return True


def click_to_first_search_tab():
    try:
        click_to_element(driver=driver,
                         element=driver.find_element(by=By.CLASS_NAME,
                                                     value="search-business-snippet-view__head"))
        time.sleep(4)
    except:
        pass


def get_workload():
    _d: dict = {}
    try:
        driver.execute_script("document.getElementsByClassName('business-attendance-view__plot-container')"
                              "[0].scrollIntoView()")
    except:
        click_to_first_search_tab()
        driver.execute_script("document.getElementsByClassName('business-attendance-view__plot-container')"
                              "[0].scrollIntoView()")

    days_of_week = find_elements(driver=driver,
                                 by=By.TAG_NAME, value="div",
                                 attribute="class", name="business-attendance-view__day")
    for day in days_of_week:
        click_to_element(driver=driver, element=day)
        time_of_day = find_elements(driver=driver,
                                    by=By.TAG_NAME, value="div",
                                    attribute="class", name="business-attendance-view__bar")
        time_of_day.pop(0)
        for t in time_of_day:
            t_r = t.get_attribute("style").replace("height: ", "")
            _d.setdefault(day.text, []).append(t_r.replace("%;", ""))
    print(_d)
    return _d


@timer
def parse_yandex_map(data: list) -> list:

    for key in range(len(data)):
        try:
            print(data[key])
            open_browser()
            input_address_in_search_window(address=data[key]["address"], sub="отделение ВТБ")

            if not is_work_office():
                data[key].update({"work": False})
                print("SKIIIIIIIIIIIIIIIIIIIIIP")
                continue

            rating = get_rating()
            workload = get_workload()

            possibilities = get_possibilities()
            permitted_operation = get_permitted_operation()

            d: dict = {"rating": rating,
                       "privilege": "privilege" in data[key],
                       "prime": "prime" in data[key],
                       "deposit_boxes": "Аренда сейфовых ячеек" in possibilities,
                       "biometric_data_collection": "Сбор биометрических данных" in possibilities,
                       "wi-fi": "Wi-Fi" in possibilities,
                       "deposit_in_rubles": "вклады в рублях" in permitted_operation,
                       "deposit_in_foreign_currency": "вклады в валюте" in permitted_operation,
                       "deposits_in_precious_metals": "вклады в драгоценных металлах" in permitted_operation,
                       "transactions_with_non-cash": "операции с безналичной валютой" in permitted_operation,
                       "cash_transactions": "операции с наличной валютой" in permitted_operation,
                       "operations_with_precious_metals": "операции с драгоценными металлами" in permitted_operation,
                       "work": True,
                       "workload": workload
                       }
            data[key].update(d)

            print(possibilities)
            print(permitted_operation)
            print(f"{key}/{len(data)}")
            print(d, "\n\n")
        except:
            print("!! - ERROR - !!")
    return data
