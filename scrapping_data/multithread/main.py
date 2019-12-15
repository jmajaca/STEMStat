import queue
import threading
import math
import subprocess

from scrapping_data.multithread import stem_driver, scrapper


def main():
    print('Program started.')
    done_queue = queue.Queue()
    driver = stem_driver.driver_init()
    try:
        max_page = get_max_page_number(driver)
    finally:
        driver.close()
    if max_page is None: exit(1)
    thread_num = int(input('Input number of threads: '))
    done_thread_num = 0
    thread_pages_num = math.floor(max_page/thread_num)
    thread_pages = []
    for i in range(thread_num):
        thread_pages.append(thread_pages_num * i + 1)
    thread_pages += [max_page + 1]
    for i in range(thread_num):
        try:
            print('Thread ' + str(i) + ' has started scraping data.')
            threading.Thread(target=scrapper.start, args=(i, thread_pages[i], thread_pages[i+1], done_queue,)).start()
        except:
            print('Thread ' + str(i) + ' has failed to start.')
    while done_thread_num != thread_num:
        # time.sleep(10)
        # see doc for timeout in queue
        last_element = done_queue.get()
        if not last_element[0]:
            print('Thread ' + str(last_element[1]) + ' has failed while scraping data.')
            response = input('Continue with scraping?[y/n]')
            if response == 'y':
                done_thread_num += 1
            elif response == 'n':
                # implement stop flag and hand it to child threads
                exit(1)
        else:
            print('Thread ' + str(last_element[1]) + ' has finished scraping data.')
            done_thread_num += 1
    subprocess.call('bash merge_results.sh', shell=True)
    print('Scrapping data is done.')


def get_max_page_number(driver):
    stem_driver.position_driver(driver)
    paginator = driver.find_element_by_id('DataTables_Table_0_paginate')
    pages = paginator.find_elements_by_class_name('paginate_button.page-item ')
    return int(pages[len(pages) - 3].text)


if __name__ == "__main__":
    main()
