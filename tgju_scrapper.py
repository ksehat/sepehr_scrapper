import datetime
import os
import json
import time
from datetime import datetime as dt
import pandas as pd
import pyodbc
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient
from persiantools import digits


class TGJUScrapper:

    def get_tgju_data(self):
        try:
            url: str = ("https://www.tgju.org/")
            options = webdriver.ChromeOptions()
            options.add_argument('--ignore-certificate-errors')
            options.add_argument('--incognito')
            options.add_argument('--headless')
            driver = webdriver.Chrome("C:\Project\Web Scraping/chromedriver", options=options)
            try:
                driver.get(url=url)
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

            for currency_num in range(1, 5):
                currency_name_list.append(driver.find_element(By.XPATH,
                                                              f'//*[@id="main"]/div[4]/div[8]/div[2]/div/div[1]/div[2]/div/div[1]/table/tbody/tr[{currency_num}]/th').text)
                currency_price_list.append(driver.find_element(By.XPATH,
                                                               f'//*[@id="main"]/div[4]/div[8]/div[2]/div/div[1]/div[2]/div/div[1]/table/tbody/tr[{currency_num}]/td[1]').text)
                currency_lowest_price_list.append(driver.find_element(By.XPATH,
                                                                      f'//*[@id="main"]/div[4]/div[8]/div[2]/div/div[1]/div[2]/div/div[1]/table/tbody/tr[{currency_num}]/td[3]').text)
                currency_highest_price_list.append(driver.find_element(By.XPATH,
                                                                       f'//*[@id="main"]/div[4]/div[8]/div[2]/div/div[1]/div[2]/div/div[1]/table/tbody/tr[{currency_num}]/td[4]').text)
                currency_price_time_list.append(datetime.datetime.now())

                df = pd.DataFrame({
                    'name': currency_name_list,
                    'price': currency_price_list,
                    'lowest': currency_lowest_price_list,
                    'highest': currency_highest_price_list,
                    'time': currency_price_time_list
                })

            result_dict = df.to_dict()

            # Connect to the MongoDB server
            MONGODB_HOST = '192.168.115.17'
            MONGODB_PORT = 27017
            MONGODB_USER = 'kanan'
            MONGODB_PASS = '123456'
            MONGODB_DB = 'fids_DB'
            client = MongoClient(MONGODB_HOST, MONGODB_PORT,
                                 username=MONGODB_USER,
                                 password=MONGODB_PASS,
                                 authSource=MONGODB_DB)

            # Get the database and collection
            db = client['currency_DB']
            collection = db['currency']
            # Insert a document
            if result_dict:
                collection.insert_many(df.to_dict('records'))

        except Exception as e:
            try:
                driver.close()
            except:
                pass
            self.get_tgju_data()

f_scrapper = TGJUScrapper()
f_scrapper.get_tgju_data()
while True:
    if (dt.now().hour == 23 and dt.now().minute == 15) or (dt.now().hour == 3 and dt.now().minute == 0) or (
            dt.now().hour == 11 and dt.now().minute == 3) or (
            dt.now().hour == 16 and dt.now().minute == 0):
        f_scrapper = TGJUScrapper()
        f_scrapper.get_tgju_data()
        time.sleep(60) # This line is necessary to not to scrape over and over again while the time is 11:00 for example.
