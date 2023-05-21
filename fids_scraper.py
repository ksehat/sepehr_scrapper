import os
import json
import schedule
import time
from datetime import datetime as dt
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
from selenium.webdriver.common.action_chains import ActionChains


def call_login_token():
    dict1 = {
        "username": "k.sehat",
        "password": "Ks@123456",
        "applicationType": 961,
        "iP": "1365"
    }
    r = requests.post(url='http://192.168.115.10:8081/api/Authentication/RequestToken',
                      json=dict1,
                      )
    token = json.loads(r.text)['token']
    expire_date = json.loads(r.text)['expires']
    return token, expire_date


def api_token_handler():
    if 'token_expire_date.txt' in os.listdir():
        with open('token_expire_date.txt', 'r') as f:
            te = f.read()
        expire_date = te.split('token:')[0]
        token = te.split('token:')[1]
        if dt.now() >= dt.strptime(expire_date, '%Y-%m-%d'):
            token, expire_date = call_login_token()
            expire_date = expire_date.split('T')[0]
            with open('token_expire_date.txt', 'w') as f:
                f.write(expire_date + 'token:' + token)
    else:
        token, expire_date = call_login_token()
        expire_date = expire_date.split('T')[0]
        with open('token_expire_date.txt', 'w') as f:
            f.write(expire_date + 'token:' + token)
    return token


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
                'Airport': [item for sublist in [x for x in airport_name_list] for item in sublist],
                'FlightDay': [item for sublist in [x[0] for x in rowed_data_list] for item in sublist],
                'Airline': [item for sublist in [x[1] for x in rowed_data_list] for item in sublist],
                'FlightNumber': [item for sublist in [x[2] for x in rowed_data_list] for item in sublist],
                'FlightOrigin': [item for sublist in [x[3] for x in rowed_data_list] for item in sublist],
                'FlightDest': [item for sublist in [x[4] for x in rowed_data_list] for item in sublist],
                'FlightStatus': [item for sublist in [x[5] for x in rowed_data_list] for item in sublist],
                'Aircraft2': [item for sublist in [x[6] for x in rowed_data_list] for item in sublist],
                'Aircraft3': [item for sublist in [x[7] for x in rowed_data_list] for item in sublist],
                'Aircraft': [item for sublist in [x[8] for x in rowed_data_list] for item in sublist],
                'Counter': [item for sublist in [x[9] for x in rowed_data_list] for item in sublist],
                'FlightDate': [item for sublist in [x[10] for x in rowed_data_list] for item in sublist],
            }
        )
        # df.to_excel(f'fids-{str(datetime.datetime.now()).split(" ")[0]}.xlsx')
        return df
    except Exception as e:
        print(f'There occured an error in the sepehr_scraper.py. {e}')
        get_booking_fids()


def job():
    token = api_token_handler()
    df = get_booking_fids()
    result_dict = {'FidsScraperBatchRequestItemViewModels':df.to_dict('records')}
    for d in result_dict['FidsScraperBatchRequestItemViewModels']:
        for k, v in d.items():
            if v is None:
                d[k] = ""
    r = requests.post(url='http://192.168.115.10:8081/api/FidsScraper/CreateFidsScraperBatch',
                      json=result_dict,
                      headers={'Authorization': f'Bearer {token}',
                               'Content-type': 'application/json',
                               })


# Schedule the job to run every 2 hours
schedule.every(1).hours.do(job)

# Schedule the job to run at 11:45 PM every day
schedule.every().day.at("23:45").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)