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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from pymongo import MongoClient


class KhalijScrapper:
    def __init__(self):
        self.last_run_num = 0
        self.url = "https://pgia.ir/components/FlightBoard.php"

    def initialize_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--incognito')
        # options.add_argument('--headless')
        self.driver = webdriver.Chrome(
            service=Service("E:\Projects\sepehr_scrapper/chromedriver.exe"),
            options=options)

    def close_driver(self):
        if self.driver:
            self.driver.quit()
            self.driver = None

    def scrape(self):
        try:
            self.initialize_driver()
            self.driver.maximize_window()
            self.driver.get(url=self.url)
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="t-arr"]')))
            terminals = ['t-dep', 't-arr']
            for terminal_in_out in terminals[self.last_run_num:]:
                self.driver.find_element(By.XPATH, f'//*[@id="{terminal_in_out}"]').click()
                if terminal_in_out == 't-dep':
                    flights_len = len(self.driver.find_elements(By.XPATH, f'//*[@id="con-dep"]/div[2]/table/tbody/tr'))
                else:
                    flights_len = len(self.driver.find_elements(By.XPATH, f'//*[@id="con-arr"]/div[2]/table/tbody/tr'))
                airline = []
                flight_number = []
                flight_dest = []
                flight_orig = []
                flight_status = []
                flight_date = []
                flight_hour = []
                aircraft = []

                for flight_num in range(1,flights_len+1):
                    if 'dep' in terminal_in_out:
                        scrap_id = 'dep'
                    else:
                        scrap_id = 'arr'
                    elem = self.driver.find_element(By.XPATH, f'//*[@id="con-{scrap_id}"]/div[2]/table/tbody/tr[{flight_num}]')
                    ActionChains(self.driver).move_to_element(elem).perform()

                    try:
                        airline.append(self.driver.find_element(By.XPATH,f'//*[@id="con-{scrap_id}"]/div[2]/table/tbody/tr[{flight_num}]/td[1]').text)
                    except:
                        airline.append('')

                    try:
                        flight_number.append(self.driver.find_element(By.XPATH,f'//*[@id="con-{scrap_id}"]/div[2]/table/tbody/tr[{flight_num}]/td[2]').text)
                    except:
                        flight_number.append('')

                    try:
                        if terminal_in_out == 't-dep': #if we are scraping the input flights
                            flight_dest.append(self.driver.find_element(By.XPATH,
                                                                      f'//*[@id="con-{scrap_id}"]/div[2]/table/tbody/tr[{flight_num}]/td[3]').text)
                            flight_orig.append('PGU')
                        else:
                            flight_orig.append(self.driver.find_element(By.XPATH,
                                                                      f'//*[@id="con-arr"]/div[2]/table/tbody/tr[{flight_num}]/td[3]').text)
                            flight_dest.append('PGU')
                    except:
                        flight_dest.append('')
                        flight_orig.append('')

                    try:
                        flight_date.append(self.driver.find_element(By.XPATH,
                                                                    f'//*[@id="con-{scrap_id}"]/div[2]/table/tbody/tr[{flight_num}]/td[9]').text)
                    except:
                        flight_date.append('')

                    try:
                        flight_hour.append(self.driver.find_element(By.XPATH,
                                                                    f'//*[@id="con-{scrap_id}"]/div[2]/table/tbody/tr[{flight_num}]/td[7]').text)
                    except:
                        flight_hour.append('')

                    try:
                        flight_status.append(self.driver.find_element(By.XPATH,
                                                                         f'//*[@id="con-{scrap_id}"]/div[2]/table/tbody/tr[{flight_num}]/td[4]').text)
                    except:
                        flight_status.append('')

                    try:
                        aircraft.append(self.driver.find_element(By.XPATH,
                                                                         f'//*[@id="con-{scrap_id}"]/div[2]/table/tbody/tr[{flight_num}]/td[5]').text)
                    except:
                        aircraft.append('')



                df = pd.DataFrame(
                    {
                        'Airport': ['PGU'] * len(flight_date),
                        'FlightHour': flight_hour,
                        'Airline': airline,
                        'FlightNumber': flight_number,
                        'FlightOrigin': flight_orig,
                        'FlightDest': flight_dest,
                        'FlightStatus': flight_status,
                        'FlightDate': flight_date,
                        'Aircraft': aircraft,
                        'Scrape_date': datetime.datetime.now()
                    }
                )

                # Connect to the MongoDB server
                MONGODB_HOST = '192.168.115.17'
                MONGODB_PORT = 24048
                MONGODB_USER = 'kanan'
                MONGODB_PASS = '123456'
                MONGODB_DB = 'scrap_DB'
                client = MongoClient(MONGODB_HOST, MONGODB_PORT,
                                     username=MONGODB_USER,
                                     password=MONGODB_PASS,
                                     authSource=MONGODB_DB)
                # Get the database and collection of MongoDB
                db = client['scrap_DB']
                collection = db['khalij']
                collection.insert_many(df.to_dict('records'))
                self.last_run_num = terminals.index(terminal_in_out)
            self.close_driver()
        except Exception as e:
            try:
                self.close_driver()
            except:
                pass
            try:
                self.last_run_num = terminals.index(terminal_in_out)
            except:
                pass
            print(f'There occurred an error in the FidsScraper class. {e}')
            self.scrape()


if __name__ == "__main__":
    scraper = KhalijScrapper()
    scraper.scrape()

    while True:
        if (dt.now().hour == 23 and dt.now().minute == random.randint(1, 10)):
            # or (dt.now().hour == 11 and dt.now().minute == random.randint(1, 59))\
            # or (dt.now().hour == 16 and dt.now().minute == random.randint(1, 59)):
            # or (dt.now().hour == 3 and dt.now().minute == random.randint(1, 59)) \
            scraper = KhalijScrapper()
            scraper.scrape()
