from selenium import webdriver
import time
import selenium as se
import csv
import re
from datetime import datetime
from selenium.webdriver.common.action_chains import ActionChains
import queue


def driver_init():
    options = se.webdriver.FirefoxOptions()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.maximize_window()
    driver.implicitly_wait(10)
    return driver


def get_rank_table(driver):
    driver.get('https://stemstipendije.mzo.hr/')
    time.sleep(2)
    drop_down_btn = driver.find_element_by_id('dropDownRangListe')
    drop_down_btn.click()
    drop_down_tech = driver.find_element_by_id('tehnickeZnanosti')
    drop_down_tech.click()
    senior_years_btn = driver.find_element_by_id('viseGodine')
    senior_years_btn.click()
    time.sleep(2)
    return driver.find_element_by_id('DataTables_Table_0')


def get_max_page_number(driver):
    paginator = driver.find_element_by_id('DataTables_Table_0_paginate')
    pages = paginator.find_elements_by_class_name('paginate_button.page-item ')
    return int(pages[len(pages) - 3].text)


def table_route(driver):
    rank_table = get_rank_table(driver)
    get_max_page_number(driver)
    columns = rank_table.find_elements_by_css_selector('tr')[1].find_elements_by_css_selector('th')
    table_header = [element.text for element in columns]
    header_dict = dict()
    for element in table_header:
        header_dict[element] = []
    for page in range(get_max_page_number(driver)):
        print(page)
        time.sleep(5)
        # rank_table = driver.find_element_by_id('DataTables_Table_0')
        rows = rank_table.find_element_by_css_selector('tbody').find_elements_by_css_selector('tr')
        for row in rows:
            row_elements = row.find_elements_by_css_selector('td')
            for index in range(1, 10):
                if index == 3:
                    if re.search('.*\.{3}$', row_elements[index].text):
                        header_dict[table_header[index]].append(row_elements[index].find_element_by_css_selector('span')
                                                                .get_attribute('data-original-title').replace('\n', ''))
                    else:
                        header_dict[table_header[index]].append(row_elements[index].text.replace('\n', ''))
                else:
                    header_dict[table_header[index]].append(row_elements[index].text.replace('\n', ''))
        receiver_list = rank_table.find_elements_by_css_selector('img')
        for element in receiver_list:
            if element.get_attribute('alt') == 'Dobitnik':
                header_dict['Dobitnik'].append(True)
            else:
                header_dict['Dobitnik'].append(False)
        write_csv(table_header, header_dict)
        driver.find_element_by_id('DataTables_Table_0_next').click()


def write_csv(table_header, header_dict):
    with open('result.csv', "w") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(table_header)
        writer.writerows(zip(*[header_dict[key] for key in table_header]))


if __name__ == '__main__':
    driver = driver_init()
    try:
        table_route(driver)
    finally:
        driver.quit()
