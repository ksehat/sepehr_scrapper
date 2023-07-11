import datetime
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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient


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


class Flight724Scrapper:
    def __init__(self, orig, dest, days_num):
        self.orig = orig
        self.dest = dest
        self.days_num = days_num

    def get_flight724_route(self):
        try:
            url: str = ("http://flight724.com/")
            options = webdriver.ChromeOptions()
            options.add_argument('--ignore-certificate-errors')
            options.add_argument('--incognito')
            # options.add_argument('--headless')
            driver = webdriver.Chrome("C:\Project\Web Scraping/chromedriver", options=options)
            try:
                driver.get(url=url)
            except:
                self.get_flight724_route()
            driver.find_element(By.XPATH, '//*[@id="search_auto_from"]').send_keys(self.orig)
            driver.find_element(By.XPATH, '//*[@id="search_auto_to"]').send_keys(self.dest)
            driver.find_element(By.XPATH, '//*[@id="departing"]').click()
            driver.find_element(By.XPATH,
                                '//a[contains(@class, "weekday") and not(contains(@class, "invalid"))]').click()
            driver.find_element(By.XPATH, '//*[@id="search_submit"]').click()

            price_list = []
            type_list = []
            airline_list = []
            datetime_list = []
            cap_list = []
            extra_info = []
            class_list = []
            for n1 in range(1, len(driver.find_elements(By.XPATH, '//div[@class="resu "]')) + 1):
                elem1 = driver.find_element(By.XPATH, f'//div[@class="resu "][{n1}]')
                ActionChains(driver).move_to_element(elem1).perform()
                try:
                    price_list.append(
                        driver.find_element(By.XPATH, f'//div[@class="resu "][{n1}]/div[@class="price"]/span').text)
                except:
                    price_list.append(None)
                try:
                    type_list.append(
                        driver.find_element(By.XPATH, f'//div[@class="resu "][{n1}]/div[@class="code"]/span').text)
                except:
                    type_list.append(None)
                try:
                    datetime_list.append(
                        driver.find_element(By.XPATH, f'//div[@class="resu "][{n1}]/div[@class="date"]').text)
                except:
                    datetime_list.append(None)

                try:
                    cap_list.append(
                        driver.find_element(By.XPATH, f'//div[@class="resu "][{n1}]/div[@class="user"]').text)
                except:
                    cap_list.append(None)

                try:
                    elem11 = driver.find_element(By.XPATH, f'//div[@class="resu "][{n1}]/div[@class="code"]')
                    ActionChains(driver).move_to_element(elem11).perform()
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, f'//div[@class="resu "][{n1}]/div[@class="code"]')))
                    airline_list.append(driver.find_element(By.XPATH,
                                                            f'//div[@class="resu "][{n1}]/div[4]/div[1]/div[2]/div[2]/strong[2]').text)
                except:
                    airline_list.append(None)
                try:
                    # ActionChains(driver).move_to_element(elem11).perform()
                    # WebDriverWait(driver, 10).until(
                    #     EC.presence_of_element_located((By.XPATH, f'//div[@class="resu "][{n1}]/div[@class="code"]')))
                    extra_info.append(driver.find_element(By.XPATH,
                                                          f'//div[@class="resu "][{n1}]/div[4]/div[1]/div[2]/div[3]').text.split(
                        '\n'))
                except:
                    extra_info.append(None)

                try:
                    # ActionChains(driver).move_to_element(elem11).perform()
                    # WebDriverWait(driver, 10).until(
                    #     EC.presence_of_element_located((By.XPATH, f'//div[@class="resu "][{n1}]/div[@class="code"]')))
                    class_list.append(driver.find_element(By.XPATH,
                                                          f'//div[@class="resu "][{n1}]/div[4]/div[1]/div[2]/div[4]').text.split(
                        '\n')[0].split(":")[1])
                except:
                    class_list.append(None)
                elem11 = driver.find_element(By.XPATH, f'//div[@class="resu "]')
                ActionChains(driver).move_to_element(elem11).perform()

            df = pd.DataFrame({
                'price_list': price_list,
                'type_list': type_list,
                'datetime_list': datetime_list,
                'cap_list': cap_list,
                'airline_list': airline_list,
                'class_list':class_list,
                'extra_info': extra_info
            })

            result_dict = df.to_dict('records')

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
            db = client['flight724_DB']
            collection = db['flight724']

            # Insert a document
            if result_dict:
                collection.insert_many(result_dict)

        except Exception as e:
            try:
                driver.close()
            except:
                pass
            print(f'There occured an error in the sepehr_scraper.py. {e}')
            self.get_flight724_route()


f_scrapper = Flight724Scrapper('MHD', 'THR', 2)
f_scrapper.get_flight724_route()
