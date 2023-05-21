import copy
import datetime
import time
import datetime as dt
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service


def tab_scrapper(driver, tab):
    flight_day = []
    airline = []
    flight_number = []
    flight_origin = []
    flight_dest = []
    flight_status = []
    aircraft2 = []
    aircraft3 = []
    aircraft = []
    counter = []
    flight_date = []
    row_xpath = f'//div[@id="{tab}"]//tr[@class="status-default"]'
    flights_len = len(driver.find_elements(By.XPATH, row_xpath))
    for i in range(1, flights_len + 1):
        try:
            elem1 = driver.find_element(By.XPATH, row_xpath + f'[{i}]')
            ActionChains(driver).move_to_element(elem1).perform()
            flight_day.append(driver.find_element(By.XPATH, f'//div[@id="{tab}"]//tr[{i}]/td[@class="cell-day"]').text)
            airline.append(driver.find_element(By.XPATH, f'//div[@id="{tab}"]//tr[{i}]/td[@class="cell-airline"]').text)
            flight_number.append(
                driver.find_element(By.XPATH, f'//div[@id="{tab}"]//tr[{i}]/td[@class="cell-fno"]').text)
            try:
                flight_origin.append(
                    driver.find_element(By.XPATH, f'//div[@id="{tab}"]//tr[{i}]/td[@class="cell-orig"]').text)
                flight_dest.append(None)
            except:
                flight_origin.append(None)
                flight_dest.append(
                    driver.find_element(By.XPATH, f'//div[@id="{tab}"]//tr[{i}]/td[@class="cell-dest"]').text)
            flight_status.append(
                driver.find_element(By.XPATH, f'//div[@id="{tab}"]//tr[{i}]/td[@class="cell-status"]').text)
            try:
                aircraft2.append(
                    driver.find_element(By.XPATH, f'//div[@id="{tab}"]//tr[{i}]/td[@class="cell-aircraft2"]').text)
                aircraft3.append(
                    driver.find_element(By.XPATH, f'//div[@id="{tab}"]//tr[{i}]/td[@class="cell-aircraft3"]').text)
            except:
                aircraft2.append(None)
                aircraft3.append(None)
            aircraft.append(
                driver.find_element(By.XPATH, f'//div[@id="{tab}"]//tr[{i}]/td[@class="cell-aircraft"]').text)
            try:
                counter.append(
                    driver.find_element(By.XPATH, f'//div[@id="{tab}"]//tr[{i}]/td[@class="cell-counter"]').text)
            except:
                counter.append(None)
            flight_date.append(
                driver.find_element(By.XPATH, f'//div[@id="{tab}"]//tr[{i}]/td[@class="cell-date"]').text)
        except:
            continue
    return [flight_day, airline, flight_number, flight_origin, flight_dest, flight_status, aircraft, aircraft2,
            aircraft3, counter, flight_date]


def in_out_flights_scrapper(driver, xpath):
    tab_xpath = f'//div[@class="tab"]/button'
    tabs_len = len(driver.find_elements(By.XPATH, xpath))
    tabs_list = ['input', 'output', 'internal', 'external']
    data = []
    for i in range(1, tabs_len + 1):
        tab = tabs_list[i - 1]
        elem1 = driver.find_element(By.XPATH, tab_xpath + f'[{i}]')
        ActionChains(driver).move_to_element(elem1).click(elem1).perform()
        data.append(tab_scrapper(driver, tab))
    return data


def get_booking_fids():
    try:
        url: str = ("https://fids.airport.ir/")
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--incognito')
        # options.add_argument('--headless')
        driver = webdriver.Chrome("C:\Project\Web Scraping/chromedriver", chrome_options=options)
        driver.get(url=url)

        airports_len = len(driver.find_elements(By.XPATH, '//li[@class=""]'))
        data_list = []
        airport = []
        for i in range(airports_len + 1):
            if i == 0:
                elem1 = driver.find_element(By.XPATH, f'//li[@class="active"]')
                airport.append(elem1.text)
                data_list.append(in_out_flights_scrapper(driver, f'//div[@class="tab"]/button'))
            else:
                elem1 = driver.find_element(By.XPATH, f'//li[@class=""][{i}]')
                airport.append(elem1.text)
                ActionChains(driver).move_to_element(elem1).click(elem1).perform()
                data_list.append(in_out_flights_scrapper(driver, f'//div[@class="tab"]/button'))

        airport_name_list = []
        for idx, airport1 in enumerate(data_list):
            for tab1 in airport1:
                flights1 = len(tab1[0])
                airport_name_list.append([airport[idx]] * flights1)

        rowed_data_list = []
        for x in data_list:
            for y in range(4):
                try:
                    rowed_data_list.append(x[y])
                except:
                    continue


        df = pd.DataFrame(
            {
                'airport': [item for sublist in [x for x in airport_name_list] for item in sublist],
                'flight_day': [item for sublist in [x[0] for x in rowed_data_list] for item in sublist],
                'airline': [item for sublist in [x[1] for x in rowed_data_list] for item in sublist],
                'flight_number': [item for sublist in [x[2] for x in rowed_data_list] for item in sublist],
                'flight_origin': [item for sublist in [x[3] for x in rowed_data_list] for item in sublist],
                'flight_dest': [item for sublist in [x[4] for x in rowed_data_list] for item in sublist],
                'flight_status': [item for sublist in [x[5] for x in rowed_data_list] for item in sublist],
                'aircraft2': [item for sublist in [x[6] for x in rowed_data_list] for item in sublist],
                'aircraft3': [item for sublist in [x[7] for x in rowed_data_list] for item in sublist],
                'aircraft': [item for sublist in [x[8] for x in rowed_data_list] for item in sublist],
                'counter': [item for sublist in [x[9] for x in rowed_data_list] for item in sublist],
                'flight_date': [item for sublist in [x[10] for x in rowed_data_list] for item in sublist],
            }
        )
        # df.to_excel(f'fids-{str(datetime.datetime.now()).split(" ")[0]}.xlsx')
        return df
    except Exception as e:
        print(f'There occured an error in the sepehr_scraper.py. {e}')
        return None


a = get_booking_fids()
