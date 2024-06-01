import os
import json
import time
import random
import datetime
from datetime import datetime as dt
import pandas as pd
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
from selenium.webdriver.common.action_chains import ActionChains
from pymongo import MongoClient


class FidsScraper:
    def __init__(self):
        self.last_run_num = 1
        self.url = "https://fids.airport.ir"
        self.driver = None

    def initialize_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--incognito')
        # options.add_argument('--headless')
        self.driver = webdriver.Chrome(
            service=Service("C:/Users/Administrator/Desktop/Projects/chromedriver.exe"),
            options=options)

    def close_driver(self):
        if self.driver:
            self.driver.quit()
            self.driver = None

    def scrape(self):
        try:
            self.initialize_driver()
            self.driver.get(url=self.url)
            airports_len = len(self.driver.find_elements(By.XPATH, '(//ul[@class="nav navbar-nav "]/li)'))

            if airports_len + 1 > self.last_run_num:
                for var1 in range(self.last_run_num, airports_len + 1):
                    airport = []
                    time.sleep(random.randint(10, 30))
                    try:
                        self.driver.find_element(By.XPATH, f'(//ul[@class="nav navbar-nav "]/li)[{var1}]').click()
                    except Exception as e:
                        try:
                            self.close_driver()
                        except:
                            pass
                        try:
                            self.last_run_num = var1
                        except:
                            pass
                        print(f'There occurred an error in the FidsScraper class. {e}')
                        self.scrape()
                    elem1 = self.driver.find_element(By.XPATH, f'(//ul[@class="nav navbar-nav "]/li)[{var1}]')
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
                    tabs_list = self.driver.find_elements(By.XPATH,
                                                          '//button[@class="tablinks" or @class="tablinks active"]')
                    for var2 in range(1, len(tabs_list) + 1):
                        if var2 == 1:
                            tab_name = 'input'
                        if var2 == 2:
                            tab_name = 'output'
                        if var2 == 3:
                            tab_name = 'internal'
                        if var2 == 4:
                            tab_name = 'external'
                        try:
                            elem2 = self.driver.find_element(By.XPATH, f'(//div[@class="tab"]/button)[{var2}]')
                            elem2.click()
                            len_flights = len(self.driver.find_elements(By.XPATH,
                                                                        f'//div[@id="{tab_name}"]/table/tbody/tr[@class="status-default"]'))
                            for var3 in range(1, len_flights + 1):
                                elem3 = self.driver.find_element(By.XPATH,
                                                                 f'(//div[@id="{tab_name}"]/table/tbody/tr[@class="status-default"])[{var3}]')
                                ActionChains(self.driver).move_to_element(elem3).perform()

                                try:
                                    flight_day.append(
                                        self.driver.find_element(By.XPATH,
                                                                 f'(//div[@id="{tab_name}"]/table/tbody/tr[@class="status-default"])[{var3}]/td[@class="cell-day"]').text)
                                except:
                                    flight_day.append('')
                                try:
                                    airline.append(
                                        self.driver.find_element(By.XPATH, f'(//div[@id="{tab_name}"]/table/tbody/tr[@class="status-default"])[{var3}]/'
                                                                           f'td[@class="cell-airline"]').text)
                                except:
                                    airline.append('')
                                try:
                                    flight_number.append(
                                        self.driver.find_element(By.XPATH, f'(//div[@id="{tab_name}"]/table/tbody/tr[@class="status-default"])[{var3}]/'
                                                                           f'td[@class="cell-fno"]').text)
                                except:
                                    flight_number.append('')
                                try:
                                    flight_origin.append(
                                        self.driver.find_element(By.XPATH, f'(//div[@id="{tab_name}"]/table/tbody/tr[@class="status-default"])[{var3}]/'
                                                                           f'td[@class="cell-orig"]').text)
                                except:
                                    flight_origin.append('')
                                try:
                                    flight_dest.append(
                                        self.driver.find_element(By.XPATH, f'(//div[@id="{tab_name}"]/table/tbody/tr[@class="status-default"])[{var3}]/'
                                                                           f'td[@class="cell-dest"]').text)
                                except:
                                    flight_dest.append('')
                                try:
                                    flight_status.append(
                                        self.driver.find_element(By.XPATH, f'(//div[@id="{tab_name}"]/table/tbody/tr[@class="status-default"])[{var3}]/'
                                                                           f'td[@class="cell-status"]').text)
                                except:
                                    flight_status.append('')
                                try:
                                    aircraft2.append(
                                        self.driver.find_element(By.XPATH, f'(//div[@id="{tab_name}"]/table/tbody/tr[@class="status-default"])[{var3}]/'
                                                                           f'td[@class="cell-aircraft2"]').text)
                                except:
                                    aircraft2.append('')
                                try:
                                    aircraft3.append(
                                        self.driver.find_element(By.XPATH, f'(//div[@id="{tab_name}"]/table/tbody/tr[@class="status-default"])[{var3}]/'
                                                                           f'td[@class="cell-aircraft3"]').text)
                                except:
                                    aircraft3.append('')
                                try:
                                    aircraft.append(
                                        self.driver.find_element(By.XPATH, f'(//div[@id="{tab_name}"]/table/tbody/tr[@class="status-default"])[{var3}]/'
                                                                           f'td[@class="cell-aircraft"]').text)
                                except:
                                    aircraft.append('')
                                try:
                                    counter.append(
                                        self.driver.find_element(By.XPATH, f'(//div[@id="{tab_name}"]/table/tbody/tr[@class="status-default"])[{var3}]/'
                                                                           f'td[@class="cell-counter"]').text)
                                except:
                                    counter.append('')
                                try:
                                    flight_date.append(
                                        self.driver.find_element(By.XPATH, f'(//div[@id="{tab_name}"]/table/tbody/tr[@class="status-default"])[{var3}]/'
                                                                           f'td[@class="cell-date"]').text)
                                except:
                                    flight_date.append('')

                        except Exception as e:
                            try:
                                self.close_driver()
                            except:
                                pass
                            try:
                                self.last_run_num = var1
                            except:
                                pass
                            print(f'There occurred an error in the FidsScraper class. {e}')
                            self.scrape()

                    # df = pd.DataFrame()
                    flight_day_list = [x3.rsplit(' ', maxsplit=1)[0] for x3 in flight_day]
                    flight_hour_list = [x3.rsplit(' ', maxsplit=1)[1] for x3 in flight_day]
                    df = pd.DataFrame(
                        {
                            'Airport': airport * len(flight_day),
                            'FlightDay': flight_day_list,
                            'FlightHour': flight_hour_list,
                            'Airline': airline,
                            'FlightNumber': flight_number,
                            'FlightOrigin': flight_origin,
                            'FlightDest': flight_dest,
                            'FlightStatus': flight_status,
                            'Aircraft2': aircraft2,
                            'ArrivalTime': aircraft3,
                            'Aircraft': aircraft,
                            'Counters': counter,
                            'FlightDate': flight_date,
                            'Scrape_date': datetime.datetime.now()
                        }
                    )

                    result_dict = df.to_dict('records')
                    result_dict_final = {'FidsScraperBatchRequestItemViewModels': result_dict}
                    for d in result_dict_final['FidsScraperBatchRequestItemViewModels']:
                        for k, v in d.items():
                            if v is None:
                                d[k] = ""

                    # r = requests.post(url='http://192.168.115.10:8081/api/FidsScraper/CreateFidsScraperBatch',
                    #                   json=result_dict,
                    #                   headers={'Authorization': f'Bearer {token}',
                    #                            'Content-type': 'application/json',
                    #                            })

                    # Connect to the MongoDB server
                    MONGODB_HOST = '192.168.115.17'
                    MONGODB_PORT = 24048
                    MONGODB_USER = 'kanan'
                    MONGODB_PASS = '123456'
                    MONGODB_DB = 'fids_DB'
                    client = MongoClient(MONGODB_HOST, MONGODB_PORT,
                                         username=MONGODB_USER,
                                         password=MONGODB_PASS,
                                         authSource=MONGODB_DB)
                    # Get the database and collection of MongoDB
                    db = client['fids_DB']
                    collection = db['fids2']

                    if result_dict_final['FidsScraperBatchRequestItemViewModels']:
                        collection.insert_many(result_dict_final['FidsScraperBatchRequestItemViewModels'])

                    self.last_run_num = var1
                    print(elem1.text)
            else:
                self.close_driver()
                self.scrape()

        except Exception as e:
            try:
                self.close_driver()
            except:
                pass
            try:
                self.last_run_num = var1
            except:
                pass
            print(f'There occurred an error in the FidsScraper class. {e}')
            self.scrape()


if __name__ == "__main__":
    scraper = FidsScraper()
    scraper.scrape()

    while True:
        if (dt.now().hour == 23 and dt.now().minute == random.randint(1, 10)):
            # or (dt.now().hour == 11 and dt.now().minute == random.randint(1, 59))\
            # or (dt.now().hour == 16 and dt.now().minute == random.randint(1, 59)):
            # or (dt.now().hour == 3 and dt.now().minute == random.randint(1, 59)) \
            scraper = FidsScraper()
            scraper.scrape()
