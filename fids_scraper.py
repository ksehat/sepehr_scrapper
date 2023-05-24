import datetime
import os
import json
import schedule
import time
from datetime import datetime as dt
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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


def get_booking_fids():
    global last_run_num
    try:
        url: str = ("https://fids.airport.ir/")
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--incognito')
        # options.add_argument('--headless')
        driver = webdriver.Chrome("C:\Project\Web Scraping/chromedriver", chrome_options=options)
        try:
            driver.get(url=url)
        except:
            get_booking_fids()
        airports_len = len(driver.find_elements(By.XPATH, '(//ul[@class="nav navbar-nav "]/li)'))
        if airports_len + 1 > last_run_num:
            for var1 in range(last_run_num, airports_len + 1):
                airport = []
                # ActionChains(driver).move_to_element(driver.find_element(By.XPATH, f'(//ul[@class="nav navbar-nav "]/li)[{i}]')).perform()
                driver.find_element(By.XPATH, f'(//ul[@class="nav navbar-nav "]/li)[{var1}]').click()
                elem1 = driver.find_element(By.XPATH, f'(//ul[@class="nav navbar-nav "]/li)[{var1}]')
                airport.append(elem1.text)

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
                for var2 in range(1, 5):
                    try:
                        # clicking on each tab
                        elem2 = driver.find_element(By.XPATH, f'(//div[@class="tab"]/button)[{var2}]')
                        # in_out_internal_external_list.append(elem2.text)
                        elem2.click()

                        len_flights = len(driver.find_elements(By.XPATH, '(//tr[@class="status-default"])'))
                        # click on each row
                        for var3 in range(1, len_flights + 1):
                            try:
                                elem3 = driver.find_element(By.XPATH, f'(//tr[@class="status-default"])[{var3}]')
                                ActionChains(driver).move_to_element(elem3).click().perform()

                                try:
                                    flight_day.append(
                                        driver.find_element(By.XPATH, f'(//tr[@class="status-default"])[{var3}]/'
                                                                      f'td[@class="cell-day"]').text)
                                except:
                                    flight_day.append('')
                                try:
                                    airline.append(
                                        driver.find_element(By.XPATH, f'(//tr[@class="status-default"])[{var3}]/'
                                                                      f'td[@class="cell-airline"]').text)
                                except:
                                    airline.append('')
                                try:
                                    flight_number.append(
                                        driver.find_element(By.XPATH, f'(//tr[@class="status-default"])[{var3}]/'
                                                                      f'td[@class="cell-fno"]').text)
                                except:
                                    flight_number.append('')
                                try:
                                    flight_origin.append(
                                        driver.find_element(By.XPATH, f'(//tr[@class="status-default"])[{var3}]/'
                                                                      f'td[@class="cell-orig"]').text)
                                except:
                                    flight_origin.append('')
                                try:
                                    flight_dest.append(
                                        driver.find_element(By.XPATH, f'(//tr[@class="status-default"])[{var3}]/'
                                                                      f'td[@class="cell-dest"]').text)
                                except:
                                    flight_dest.append('')
                                try:
                                    flight_status.append(
                                        driver.find_element(By.XPATH, f'(//tr[@class="status-default"])[{var3}]/'
                                                                      f'td[@class="cell-status"]').text)
                                except:
                                    flight_status.append('')
                                try:
                                    aircraft2.append(
                                        driver.find_element(By.XPATH, f'(//tr[@class="status-default"])[{var3}]/'
                                                                      f'td[@class="cell-aircraft2"]').text)
                                except:
                                    aircraft2.append('')
                                try:
                                    aircraft3.append(
                                        driver.find_element(By.XPATH, f'(//tr[@class="status-default"])[{var3}]/'
                                                                      f'td[@class="cell-aircraft3"]').text)
                                except:
                                    aircraft3.append('')
                                try:
                                    aircraft.append(
                                        driver.find_element(By.XPATH, f'(//tr[@class="status-default"])[{var3}]/'
                                                                      f'td[@class="cell-aircraft"]').text)
                                except:
                                    aircraft.append('')
                                try:
                                    counter.append(
                                        driver.find_element(By.XPATH, f'(//tr[@class="status-default"])[{var3}]/'
                                                                      f'td[@class="cell-counter"]').text)
                                except:
                                    counter.append('')
                                try:
                                    flight_date.append(
                                        driver.find_element(By.XPATH, f'(//tr[@class="status-default"])[{var3}]/'
                                                                      f'td[@class="cell-date"]').text)
                                except:
                                    flight_date.append('')
                            except:
                                continue

                    except:
                        continue
                df = pd.DataFrame()
                df = pd.DataFrame(
                    {
                        'Airport': airport * len(flight_day),
                        'FlightDay': flight_day,
                        'Airline': airline,
                        'FlightNumber': flight_number,
                        'FlightOrigin': flight_origin,
                        'FlightDest': flight_dest,
                        'FlightStatus': flight_status,
                        'Aircraft2': aircraft2,
                        'Aircraft3': aircraft3,
                        'Aircraft': aircraft,
                        'Counter': counter,
                        'FlightDate': flight_date,
                    }
                )
                miladi_shamsi_dict = {
                    "Saturday": "شنبه",
                    "Sunday": "یکشنبه",
                    "Monday": "دو شنبه",
                    "Tuesday": "سه شنبه",
                    "Wednesday": "چهار شنبه",
                    "Wednesday": "چهارشنبه",
                    "Thursday": "پنجشنبه",
                    "Friday": "جمعه"
                }
                token = api_token_handler()
                today = miladi_shamsi_dict[str(datetime.datetime.now().strftime('%A'))]
                result_dict = df.to_dict('records')
                result_dict_final = [d1 for d1 in result_dict if today in d1["FlightDay"]]

                result_dict = {'FidsScraperBatchRequestItemViewModels': result_dict_final}
                for d in result_dict['FidsScraperBatchRequestItemViewModels']:
                    for k, v in d.items():
                        if v is None:
                            d[k] = ""

                r = requests.post(url='http://192.168.115.10:8081/api/FidsScraper/CreateFidsScraperBatch',
                                  json=result_dict,
                                  headers={'Authorization': f'Bearer {token}',
                                           'Content-type': 'application/json',
                                           })
        else:
            driver.close()
            get_booking_fids()
    except Exception as e:
        try:
            driver.close()
        except:
            pass
        try:
            last_run_num = var1
        except:
            pass
        print(f'There occured an error in the sepehr_scraper.py. {e}')
        get_booking_fids()



while True:
    if dt.now().hour == 23 and dt.now().minute == 40:
        last_run_num = 1
        get_booking_fids()
