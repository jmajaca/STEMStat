import time
import csv
import re

from typing import Final
from scrapping_data.multithread import stem_driver

wait_time: Final = 15


def scrap_data(driver, thread_num, start_page, end_page, done_queue):
    stem_driver.position_driver(driver)
    rank_table = driver.find_element_by_id('DataTables_Table_0')
    columns = rank_table.find_elements_by_css_selector('tr')[1].find_elements_by_css_selector('th')
    table_header = [element.text for element in columns]
    header_dict = dict()
    for element in table_header:
        header_dict[element] = []
    driver.find_element_by_id('stranica').send_keys(start_page)
    # time.sleep(15)
    for page in range(start_page, end_page):
        time.sleep(wait_time)
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
        write_csv(table_header, header_dict, thread_num)
        driver.find_element_by_id('DataTables_Table_0_next').click()
        # time.sleep(15)
    done_queue.put((True, thread_num))


def write_csv(table_header, header_dict, thread_num):
    filename = 'result' + str(thread_num) + '.csv'
    with open(filename, "w") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        if thread_num == 0: writer.writerow(table_header)
        writer.writerows(zip(*[header_dict[key] for key in table_header]))


def start(thread_num, start_page, end_page, done_queue):
    driver = stem_driver.driver_init()
    try:
        scrap_data(driver, thread_num, start_page, end_page, done_queue)
    except:
        done_queue.put((False, thread_num))
    finally:
        driver.quit()
