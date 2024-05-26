import datetime
import pandas as pd
import os
import json
import time
from datetime import datetime as dt
import pandas as pd
# import pyodbc
from selenium import webdriver
from selenium.webdriver.common.by import By
# import requests
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from pymongo import MongoClient
import subprocess


class TGJUScrapper:
    def __init__(self, url):
        self.url = url

    def get_tgju_data(self):
        try:
            options = webdriver.ChromeOptions()
            options.add_argument('--ignore-certificate-errors')
            options.add_argument('--incognito')
            # options.add_argument('--headless')
            service = Service("E:\Projects\chromedriver/chromedriver.exe")
            driver = webdriver.Chrome(service=service, options=options)
            try:
                driver.get(url=self.url)
            except:
                self.get_tgju_data()
            try:
                driver.find_element(By.XPATH, '//*[@id="tgju-notification"]/div[2]/div/button[2]').click()
            except:
                pass
            try:
                driver.find_element(By.XPATH, '//*[@id="popup-layer-container"]/div[2]/a').click()
            except:
                pass
            currency_name_list = []
            currency_price_list = []
            currency_lowest_price_list = []
            currency_highest_price_list = []
            currency_price_time_list = []

            elem1 = driver.find_element(By.XPATH,
                                        f'//*[@id="main"]/div[4]/div[8]/div[2]/div/div[1]/div[2]/div/div[1]/table/tbody')
            ActionChains(driver).move_to_element(elem1).perform()
            scraping_dict = {'div[1]':[1,2,3,16], 'div[2]':[7]}
            for k,v in scraping_dict.items():
                for currency_num in v:
                    elem1 = driver.find_element(By.XPATH,
                                                f'//*[@id="main"]/div[4]/div[8]/div[2]/div/div[1]/div[2]/div/{k}/table/tbody/tr[{currency_num}]')
                    ActionChains(driver).move_to_element(elem1).perform()
                    currency_name_list.append(driver.find_element(By.XPATH,
                                                                  f'//*[@id="main"]/div[4]/div[8]/div[2]/div/div[1]/div[2]/div/{k}/table/tbody/tr[{currency_num}]/th').text)
                    currency_price_list.append(driver.find_element(By.XPATH,
                                                                   f'//*[@id="main"]/div[4]/div[8]/div[2]/div/div[1]/div[2]/div/{k}/table/tbody/tr[{currency_num}]/td[1]').text)
                    currency_lowest_price_list.append(driver.find_element(By.XPATH,
                                                                          f'//*[@id="main"]/div[4]/div[8]/div[2]/div/div[1]/div[2]/div/{k}/table/tbody/tr[{currency_num}]/td[3]').text)
                    currency_highest_price_list.append(driver.find_element(By.XPATH,
                                                                           f'//*[@id="main"]/div[4]/div[8]/div[2]/div/div[1]/div[2]/div/{k}/table/tbody/tr[{currency_num}]/td[4]').text)
                    currency_price_time_list.append(datetime.datetime.now())


            df = pd.DataFrame({
                'currency': currency_name_list,
                'price': currency_price_list,
                'low': currency_lowest_price_list,
                'high': currency_highest_price_list,
                'scrape_date': currency_price_time_list
            })
            mapping = {'دلار': 'usd', 'یورو': 'eur', 'درهم امارات': 'aed', 'دینار عراق': 'iqd', 'دینار کویت': 'kwd'}
            df['currency'] = df['currency'].replace(mapping)

            # Connect to the MongoDB server
            MONGODB_HOST = '192.168.115.17'
            MONGODB_PORT = 24048
            MONGODB_USER = 'kanan'
            MONGODB_PASS = '123456'
            MONGODB_DB = 'tgju_DB'
            client = MongoClient(MONGODB_HOST, MONGODB_PORT,
                                 username=MONGODB_USER,
                                 password=MONGODB_PASS,
                                 authSource=MONGODB_DB)

            # Get the database and collection
            db = client['tgju_DB']
            collection = db['currency']
            # Insert a document
            if not df.empty:
                collection.insert_many(df.to_dict('records'))

        except Exception as e:
            try:
                driver.close()
            except:
                pass
            self.get_tgju_data()

    def get_historical_data(self, num_of_pages):
        MONGODB_HOST = '192.168.115.17'
        MONGODB_PORT = 24048
        MONGODB_USER = 'kanan'
        MONGODB_PASS = '123456'
        MONGODB_DB = 'tgju_DB'
        client = MongoClient(MONGODB_HOST, MONGODB_PORT,
                             username=MONGODB_USER,
                             password=MONGODB_PASS,
                             authSource=MONGODB_DB)
        # Get the database and collection of MongoDB
        db = client['tgju_DB']
        collection = db['history']

        options = webdriver.ChromeOptions()
        # options.add_argument('--ignore-certificate-errors')
        options.add_argument('--incognito')
        service = Service("E:\Projects\chromedriver\chromedriver-win64/chromedriver.exe")
        # options.add_argument('--headless')
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(url=self.url)
        time.sleep(2)
        for page in range(num_of_pages):
            if not page == 0:
                elem_temp = driver.find_element(By.XPATH, '//*[@id="DataTables_Table_0_next"]')
                ActionChains(driver).move_to_element(elem_temp).click().perform()
            open_list = []
            low_list = []
            high_list = []
            close_list = []
            sun_cal_list = []
            gregorian_cal_list = []
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "table-list")))
            time.sleep(2)
            rows_num = len(driver.find_elements(By.XPATH, '//tr[@role="row"]'))
            for elem in range(1, rows_num + 1):
                try:
                    info_row = driver.find_element(By.XPATH, f'//tbody/tr[@role="row"][{elem}]').text.split(' ')
                except:
                    continue
                if len(info_row) == 8:
                    open_list.append(info_row[0])
                    low_list.append(info_row[1])
                    high_list.append(info_row[2])
                    close_list.append(info_row[3])
                    gregorian_cal_list.append(info_row[6])
                    sun_cal_list.append(info_row[7])
                else:
                    continue
            df_page_table = pd.DataFrame({
                'currency': [driver.find_element(By.XPATH,'//*[@id="main"]/div[1]/div[1]/div[1]/div/div[1]/div[2]/div[2]/div').text.lower()] * len(open_list),
                'open': open_list,
                'low': low_list,
                'high': high_list,
                'close': close_list,
                'sun_cal': sun_cal_list,
                'gregorian_cal': gregorian_cal_list,
                'scrape_date': [datetime.datetime.now()] * len(open_list)
            })

            collection.insert_many(df_page_table.to_dict('records'))
            print(page)


# f_scrapper = TGJUScrapper("https://www.tgju.org/")
# f_scrapper.get_tgju_data()
# while True:
#     if (dt.now().hour == 23 and dt.now().minute == 45):# or (dt.now().hour == 3 and dt.now().minute == 0) or (
#             # dt.now().hour == 11 and dt.now().minute == 3) or (
#             # dt.now().hour == 16 and dt.now().minute == 0):
#         f_scrapper = TGJUScrapper("https://www.tgju.org/")
#         f_scrapper.get_tgju_data()
#         time.sleep(
#             60)  # This line is necessary to not to scrape over and over again while the time is 11:00 for example.

for currency in ['aed', 'eur', 'iqd', 'kwd', 'dollar_rl']:
    # currency = 'dollar_rl'
    try:
        f_scrapper = TGJUScrapper(f'https://www.tgju.org/profile/price_{currency}/history')
        f_scrapper.get_historical_data(num_of_pages=1)
    except:
        continue
