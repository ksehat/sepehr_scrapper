import re
import datetime
import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from pymongo import MongoClient
from selenium.webdriver.chrome.service import Service


class FlyTodayScrapper:
    def __init__(self, orig, dest, days_num=None, scraping_date=None, id_from_backend=None):
        self.orig = orig
        self.dest = dest
        self.days_num = days_num
        self.error_exit = 0
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument('--incognito')
        self.options.add_argument("--disable-popup-blocking")
        self.scraping_date = scraping_date
        self.id_from_backend = id_from_backend

    def get_flytoday_route_by_date(self):
        try:
            self.driver = webdriver.Chrome(service=Service(
                "E:\Projects\sepehr_scrapper\chromedriver.exe"), options=self.options)

            for self.day_counter in range(10,self.days_num):
                try:
                    if not self.scraping_date:
                        flight_date = str(datetime.datetime.now() + datetime.timedelta(days=self.day_counter)).split(" ")[0]
                    else:
                        try:
                            flight_date = self.scraping_date.split(' ')[0]
                        except:
                            flight_date = self.scraping_date
                    self.driver.get(
                        url=f'https://www.flytoday.ir/flight/search?departure={self.orig},1&arrival={self.dest},1&departureDate={flight_date}&adt=1&chd=0&inf=0&cabin=1&isDomestic=true')
                    try:
                        WebDriverWait(self.driver, 20).until(EC.frame_to_be_available_and_switch_to_it('webpush-onsite'))
                        self.driver.find_element(By.XPATH, '//*[@id="deny"]').click()
                        self.driver.switch_to.default_content()
                    except:
                        pass
                    orig_list = []
                    dest_list = []
                    days_num_list = []
                    price_list = []
                    flight_num_list = []
                    ticket_type_list = []
                    airline_list = []
                    cap_list = []
                    dep_list = []
                    arr_list = []
                    price_class_list = []
                    cabin_type_list = []
                    airplane_model_list = []
                    selling_type_list = []
                    WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, '//div[@class="itinerary_wrapper__NZYJF  "]')))
                    for n1 in range(1,
                                    len(self.driver.find_elements(By.XPATH,
                                                                  '//div[@class="itinerary_wrapper__NZYJF  "]')) + 1):
                        elem1 = self.driver.find_element(By.XPATH, f'//div[@class="itinerary_wrapper__NZYJF  "][{n1}]')
                        ActionChains(self.driver).move_to_element(elem1).perform()
                        orig_list.append(self.orig)
                        dest_list.append(self.dest)
                        days_num_list.append(self.days_num)
                        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH,
                                                                                             '//*[@id="__next"]/div[4]/div[4]/div/div[2]/div/div[3]/div[1]/div/div/div[1]/div/div[2]/div/div/div[2]/div[1]/div[1]/div')))
                        try:
                            price_list.append(
                                self.driver.find_element(By.XPATH,
                                                         f'//*[@id="__next"]/div[4]/div[4]/div/div[2]/div/div[3]/div[{n1}]/div/div/div[2]/div[1]/div/div').text)
                        except:
                            price_list.append(None)

                        try:
                            ticket_type_list.append(
                                self.driver.find_element(By.XPATH,
                                                         f'//*[@id="__next"]/div[4]/div[4]/div/div[2]/div/div[3]/div[{n1}]/div/div/div[1]/div/div[2]/div/div/div[2]/div[4]/div[2]/div/div/span').text)
                        except:
                            ticket_type_list.append(None)
                        try:
                            dep_list.append(
                                self.driver.find_element(By.XPATH,
                                                         f'//*[@id="__next"]/div[4]/div[4]/div/div[2]/div/div[3]/div[{n1}]/div/div/div[1]/div/div[2]/div/div/div[2]/div[1]/div[1]/div').text)
                        except:
                            dep_list.append(None)
                        try:
                            arr_list.append(
                                self.driver.find_element(By.XPATH,
                                                         f'//*[@id="__next"]/div[4]/div[4]/div/div[2]/div/div[3]/div[{n1}]/div/div/div[1]/div/div[2]/div/div/div[2]/div[3]/div[1]/div').text)
                        except:
                            arr_list.append(None)
                        try:
                            cap_list.append(
                                self.driver.find_element(By.XPATH,
                                                         f'//*[@id="__next"]/div[4]/div[4]/div/div[2]/div/div[3]/div[{n1}]/div/div/div[1]/div/div[2]/div/div/div[2]/div[4]/div[3]/span[1]').text)
                        except:
                            cap_list.append(None)

                        try:
                            selling_type = self.driver.find_element(By.XPATH,
                                                                    f'//*[@id="__next"]/div[4]/div[4]/div/div[2]/div/div[3]/div[{n1}]/div/div/div[1]/div/div[1]/div').text
                            if '\n' not in selling_type:
                                selling_type_list.append(selling_type)
                            else:
                                selling_type_list.append(None)
                        except:
                            selling_type_list.append(None)

                        try:
                            airline_list.append(self.driver.find_element(By.XPATH,
                                                                         f'//*[@id="__next"]/div[4]/div[4]/div/div[2]/div/div[3]/div[{n1}]/div/div/div[1]/div/div/div/div/div[1]/div/div[2]/div[1]/p').text)
                        except:
                            airline_list.append(None)
                        try:
                            flight_num_list.append(self.driver.find_element(By.XPATH,
                                                                            f'//*[@id="__next"]/div[4]/div[4]/div/div[2]/div/div[3]/div[{n1}]/div/div/div[1]/div/div/div/div/div[1]/div/div[2]/div[2]/p').text)
                        except:
                            flight_num_list.append(None)

                        self.driver.find_element(By.XPATH,
                                                 f'//*[@id="__next"]/div[4]/div[4]/div/div[2]/div/div[3]/div[{n1}]/div/div/div[2]/div[2]/div[2]/button').click()
                        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                            (By.XPATH, '//*[@id="modals-portal"]/div/div/div[2]/div[1]/div/div')))
                        try:
                            cabin_type_list.append(self.driver.find_element(By.XPATH,
                                                                            '//*[@id="modals-portal"]/div/div/div[2]/div[1]/div/div/div/div/div[3]/div[5]/span[2]').text)
                        except:
                            cabin_type_list.append(None)
                        try:
                            price_class_list.append(self.driver.find_element(By.XPATH,
                                                                             '//*[@id="modals-portal"]/div/div/div[2]/div[1]/div/div/div/div/div[3]/div[6]/span[2]').text)
                        except:
                            price_class_list.append(None)
                        try:
                            airplane_model_list.append(self.driver.find_element(By.XPATH,
                                                                                '//*[@id="modals-portal"]/div/div/div[2]/div[1]/div/div/div/div/div[3]/div[3]/span[3]').text)
                        except:
                            airplane_model_list.append(None)

                        elem11 = self.driver.find_element(By.XPATH,
                                                          f'//*[@id="__next"]/div[4]/div[4]/div/div[2]/div/div[3]/div[{n1}]/div/div/div[1]/div/div[2]/div/div/div[2]/div[1]/div[1]/div')  # click on the dep time of the current scraping div to close the side window
                        ActionChains(self.driver).move_to_element(elem11).click(elem11).perform()

                    df = pd.DataFrame({
                        'source': ['flytoday.ir'] * len(price_list),
                        'orig': orig_list,
                        'dest': dest_list,
                        'dur': days_num_list,
                        'flight_date': [flight_date] * len(price_list),
                        'price': price_list,
                        'ticket_type': ticket_type_list,
                        'dep_time': dep_list,
                        'arr_time': arr_list,
                        'capacity': cap_list,
                        'airline': airline_list,
                        'airplane_model': airplane_model_list,
                        'price_class': price_class_list,
                        'flight_num': flight_num_list,
                        'cabin_type': cabin_type_list,
                        'selling_type': selling_type_list,
                        # 'id_from_backend': [self.id_from_backend] * len(extra_info),
                        'scrap_date': [str(datetime.datetime.now())] * len(price_list)
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
                        collection = db['flytoday']
                        collection.insert_many(result_dict)
                    self.day_counter += 1
                    return df
                except:
                    try:
                        if self.driver.find_element(By.XPATH,
                                                    "//*[contains(text(), 'ظرفیت پروازها در این تاریخ تکمیل شده است')]"):
                            self.day_counter += 1
                    except:
                        return False
        except:
            try:
                self.driver.close()
            except:
                pass
            return False


f_scrapper = FlyTodayScrapper('THR', 'MHD', 13)
result = False
while result == False:
    result = f_scrapper.get_flytoday_route_by_date()
