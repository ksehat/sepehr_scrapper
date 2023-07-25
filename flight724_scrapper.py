import datetime
import os
import json
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
        self.day_num_text = None
        self.day_num = 1

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
            if self.day_num_text:
                year_temp, month_temp, day_temp = [int(x) for x in self.day_num_text.split('/')]
                driver.find_element(By.XPATH, '/html/body/div[7]/table/tbody/tr[1]/td/a[2]').click()
                driver.find_element(By.XPATH, f'//a[contains(text(), "{digits.en_to_fa(str(year_temp))}")]').click()
                driver.find_element(By.XPATH, '/html/body/div[7]/table/tbody/tr[1]/td/a[1]').click()
                driver.find_element(By.XPATH, f'//*[@id="undefinedmonthYearPicker"]/a[{month_temp}]').click()
                driver.find_element(By.XPATH,
                                    f'//a[contains(@class, "weekday") and not(contains(@class, "invalid")) and contains(text(), "{digits.en_to_fa(str(day_temp))}")]').click()
                self.day_num_text = None
            else:
                driver.find_element(By.XPATH,
                                    '//a[contains(@class, "weekday") and not(contains(@class, "invalid"))]').click()
            driver.find_element(By.XPATH, '//*[@id="search_submit"]').click()

            for day_num in range(self.day_num, self.days_num + 1):
                self.day_num_text = driver.find_element(By.XPATH, '//*[@id="r_city_date"]/span').text
                if day_num > 0:
                    WebDriverWait(driver, 3).until(
                        EC.presence_of_element_located((By.XPATH, '//a[contains(text(), "روز بعد")]')))
                    driver.find_element(By.XPATH, '//a[contains(text(), "روز بعد")]').click()
                try:
                    WebDriverWait(driver, 3).until(
                        EC.presence_of_element_located(
                            (By.XPATH, f'//div[@class="resu "]')))
                except:
                    if driver.find_element(By.XPATH, '//*[@id="fromprice"]/div[2]/div[1]').text == '0 تا ( نتیجه)':
                        continue
                    else:
                        raise 1

                orig_list = []
                dest_list = []
                price_list = []
                type_list = []
                airline_list = []
                datetime_list = []
                cap_list = []
                extra_info = []
                class_list = []
                flight_date = driver.find_element(By.XPATH, '//*[@id="r_city_date"]/span').text
                for n1 in range(1, len(driver.find_elements(By.XPATH, '//div[@class="resu "]')) + 1):
                    elem1 = driver.find_element(By.XPATH, f'//div[@class="resu "][{n1}]')
                    ActionChains(driver).move_to_element(elem1).perform()
                    orig_list.append(self.orig)
                    dest_list.append(self.dest)
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
                            EC.presence_of_element_located(
                                (By.XPATH, f'//div[@class="resu "][{n1}]/div[@class="code"]')))
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
                    'orig': orig_list,
                    'dest': dest_list,
                    'flight_date': [flight_date] * len(extra_info),
                    'price_list': price_list,
                    'type_list': type_list,
                    'datetime_list': datetime_list,
                    'cap_list': cap_list,
                    'airline_list': airline_list,
                    'class_list': class_list,
                    'extra_info': extra_info,
                    'scrap_date': [str(datetime.datetime.now())] * len(extra_info)
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

                sql_server = '192.168.40.57'
                sql_database = 'fids_mongodb'
                sql_username = 'k.sehat'
                sql_password = 'K@123456'
                cnxn = pyodbc.connect(driver='{SQL Server}',
                                      server=sql_server,
                                      database=sql_database,
                                      uid=sql_username, pwd=sql_password)
                cursor = cnxn.cursor()
                insert_stmt = "INSERT INTO FIDS_JSON (jsoncontent,SiteName) VALUES (?,?)"
                cursor.execute(insert_stmt, ('kanan3', 'sitename'))
                cnxn.commit()
                cnxn.close()
        except Exception as e:
            self.day_num = day_num - 1
            try:
                driver.close()
            except:
                pass
            print(f'There occured an error in the sepehr_scraper.py. {e}')
            self.get_flight724_route()
