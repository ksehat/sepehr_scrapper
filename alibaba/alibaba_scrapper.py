import re
import datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from pymongo import MongoClient
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.proxy import Proxy, ProxyType


class AlibabaScrapper:
    def __init__(self, orig, dest, days_num, scraping_date=None):
        self.orig = orig
        self.dest = dest
        self.days_num = days_num
        self.day_num_text = None
        self.day_num = 0
        self.error_exit = 0
        self.url: str = ("https://alibaba.ir/#")
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument('--incognito')
        self.scraping_date = scraping_date

    def get_alibaba_route(self):
        try:
            try:
                self.driver = webdriver.Chrome(service=Service(
                    "E:\Projects\sepehr_scrapper\chromedriver.exe"), options=self.options)
                self.driver.get(url=self.url)
            except:
                try:
                    self.driver.close()
                except:
                    pass
                self.get_alibaba_route()
            self.driver.find_element(By.XPATH,
                                     '//*[@id="app"]/div[1]/main/div/div[2]/div[1]/div[2]/div/form/div[2]/div[1]/div/div[1]/div[1]/span').send_keys(
                self.orig + '\n')
            self.driver.find_element(By.XPATH, '//*[@id="al136986"]').send_keys(self.dest + '\n')
            self.driver.find_element(By.XPATH,
                                     '//*[@id="app"]/div[1]/main/div/div[2]/div[1]/div[2]/div/form/div[2]/div[2]/div/div[1]/div[1]/label').click()
            self.driver.find_element(By.XPATH,
                                     '//*[@id="app"]/div[1]/main/div/div[2]/div[1]/div[2]/div/form/div[2]/div[2]/div/div[2]/div/div[1]/button[2]/span').click()
            self.driver.find_element(By.XPATH, '/html/body/div[7]/table/tbody/tr[9]/td/a').click()
            if self.day_num_text:
                self.select_date_from_calendar(self.driver, self.day_num_text)
            elif self.scraping_date:
                self.select_date_from_calendar(self.driver, self.scraping_date)
            else:
                self.driver.find_element(By.XPATH,
                                         '//a[contains(@class, "weekday") and not(contains(@class, "invalid"))]').click()
            self.driver.find_element(By.XPATH, '//*[@id="search_submit"]').click()
            for self.day_num in range(self.day_num, self.days_num):
                if self.day_num > 0 and not self.error_exit:
                    WebDriverWait(self.driver, 3).until(
                        EC.presence_of_element_located((By.XPATH, '//a[contains(text(), "روز بعد")]')))
                    self.driver.find_element(By.XPATH, '//a[contains(text(), "روز بعد")]').click()
                try:
                    self.error_exit = 0
                    WebDriverWait(self.driver, 3).until(
                        EC.presence_of_element_located(
                            (By.XPATH, f'//div[@class="resu "]')))
                except:
                    if self.driver.find_element(By.XPATH, '//*[@id="fromprice"]/div[2]/div[1]').text == '0 تا ( نتیجه)':
                        continue
                    else:
                        raise 1

                self.day_num_text = self.driver.find_element(By.XPATH, '//*[@id="r_city_date"]').text

                orig_list = []
                dest_list = []
                days_num_list = []
                price_list = []
                class_icon_list = []
                type_list = []
                airline_list = []
                datetime_list = []
                cap_list = []
                extra_info = []
                class_list = []
                flight_date = self.driver.find_element(By.XPATH, '//*[@id="r_city_date"]').text
                for n1 in range(2, len(self.driver.find_elements(By.XPATH, '//div[@class="resu "]')) + 1):
                    elem1 = self.driver.find_element(By.XPATH, f'//div[@class="resu "][{n1}]')
                    ActionChains(self.driver).move_to_element(elem1).perform()
                    orig_list.append(self.orig)
                    dest_list.append(self.dest)
                    days_num_list.append(self.days_num)
                    try:
                        price_list.append(
                            self.driver.find_element(By.XPATH, f'//div[@class="resu "][{n1}]/div[1]/span').text)
                    except:
                        price_list.append(None)

                    try:
                        class_icon_list.append(
                            self.driver.find_element(By.XPATH,
                                                     f'//div[@class="resu "][{n1}]/div[1]/div').text)
                    except:
                        class_icon_list.append(None)

                    try:
                        type_list.append(
                            self.driver.find_element(By.XPATH,
                                                     f'//div[@class="resu "][{n1}]/div[@class="code"]/span').text)
                    except:
                        type_list.append(None)
                    try:
                        datetime_list.append(
                            self.driver.find_element(By.XPATH, f'//div[@class="resu "][{n1}]/div[@class="date"]').text)
                    except:
                        datetime_list.append(None)

                    try:
                        cap_list.append(
                            self.driver.find_element(By.XPATH, f'//div[@class="resu "][{n1}]/div[@class="user"]').text)
                    except:
                        cap_list.append(None)

                    try:
                        elem11 = self.driver.find_element(By.XPATH,
                                                          f'//div[@class="resu "][{n1}]/div[4]/div[1]/div[1]/p')
                        ActionChains(self.driver).move_to_element(elem11).perform()
                        WebDriverWait(self.driver, 10).until(
                            EC.presence_of_element_located(
                                (By.XPATH, f'//div[@class="resu "][{n1}]/div[@class="code"]')))
                        airline_list.append(self.driver.find_element(By.XPATH,
                                                                     f'//div[@class="resu "][{n1}]/div[4]/div[1]/div[2]/div[2]/strong[2]').text)
                    except:
                        airline_list.append(None)
                    try:
                        # ActionChains(driver).move_to_element(elem11).perform()
                        # WebDriverWait(driver, 10).until(
                        #     EC.presence_of_element_located((By.XPATH, f'//div[@class="resu "][{n1}]/div[@class="code"]')))
                        extra_info.append(self.driver.find_element(By.XPATH,
                                                                   f'//div[@class="resu "][{n1}]/div[4]/div[1]/div[2]/div[3]').text.split(
                            '\n'))
                    except:
                        extra_info.append(None)

                    try:
                        class_list.append(" ".join(re.findall("[a-zA-Z]+", self.driver.find_element(By.XPATH,
                                                                                                    f'//div[@class="resu "][{n1}]/div[4]/div[1]/div[2]/div[4]').text)))
                    except:
                        class_list.append(None)
                    elem11 = self.driver.find_element(By.XPATH, f'//div[@class="resu "]')
                    ActionChains(self.driver).move_to_element(elem11).perform()

                df = pd.DataFrame({
                    'orig': orig_list,
                    'dest': dest_list,
                    'dur': days_num_list,
                    'class': class_icon_list,
                    'flight_date': [flight_date] * len(extra_info),
                    'price': price_list,
                    'type': type_list,
                    'datetime': datetime_list,
                    'capacity': cap_list,
                    'airline': airline_list,
                    'airplane_class': [ali[1].split(':')[1] if len(ali) >= 3 else None for ali in extra_info],
                    'total_capacity': [re.findall(r'\d+', ali[2]) if len(ali) >= 3 else None for ali in extra_info],
                    'flight_number': [ali[0].split(':')[1].replace(' ', '') if len(ali) >= 3 else None for ali in
                                      extra_info],
                    'flight_class': class_list,
                    'extra_info': extra_info,
                    'scrap_date': [str(datetime.datetime.now())] * len(extra_info)
                })

                result_dict = df.to_dict('records')
                if result_dict:
                    MONGODB_HOST = '192.168.115.17'
                    MONGODB_PORT = 24048
                    MONGODB_USER = 'kanan'
                    MONGODB_PASS = '123456'
                    MONGODB_DB = 'dp_DB'
                    client = MongoClient(MONGODB_HOST, MONGODB_PORT,
                                         username=MONGODB_USER,
                                         password=MONGODB_PASS,
                                         authSource=MONGODB_DB)

                    db = client['dp_DB']
                    collection = db['alameer']
                    collection.insert_many(result_dict)
            self.driver.close()
            return True
        except Exception as e:
            try:
                self.driver.close()
            except:
                pass
            self.error_exit = 1
            return False

    @staticmethod
    def select_date_from_calendar(driver, date_to_be_selected):
        year_temp, month_temp, day_temp = [int(x) for x in date_to_be_selected.split('-')]
        driver.find_element(By.XPATH, '/html/body/div[7]/table/tbody/tr[1]/td/a[2]').click()
        driver.find_element(By.XPATH, f'//div/a[contains(text(), "{str(year_temp)}")]').click()
        driver.find_element(By.XPATH, '/html/body/div[7]/table/tbody/tr[1]/td/a[1]').click()
        driver.find_element(By.XPATH, f'//*[@id="undefinedmonthYearPicker"]/a[{month_temp}]').click()
        driver.find_element(By.XPATH,
                            f'//a[contains(@class, "weekday") and not(contains(@class, "invalid")) and contains(text(), "{str(day_temp)}")]').click()


f_scrapper = AlibabaScrapper('THR', 'MHD', 3)
f_scrapper.get_alibaba_route()
