import selenium as se
import time

from selenium import webdriver
from typing import Final


wait_time: Final = 4


def driver_init():
    options = se.webdriver.FirefoxOptions()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.maximize_window()
    driver.implicitly_wait(10)
    return driver


def position_driver(driver):
    driver.get('https://stemstipendije.mzo.hr/')
    time.sleep(wait_time)
    drop_down_btn = driver.find_element_by_id('dropDownRangListe')
    drop_down_btn.click()
    drop_down_tech = driver.find_element_by_id('tehnickeZnanosti')
    drop_down_tech.click()
    senior_years_btn = driver.find_element_by_id('viseGodine')
    senior_years_btn.click()
    time.sleep(wait_time)
