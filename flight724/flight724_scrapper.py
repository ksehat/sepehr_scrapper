import datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient
from selenium.webdriver.chrome.service import Service


class Flight724Scrapper:
    def __init__(self, orig, dest, days_num):
        self.orig = orig
        self.dest = dest
        self.days_num = days_num
        self.day_num_text = None
        self.day_num = 0
        self.error_exit = 0
        self.orig_dest_are_extracted = False

    def get_flight724_route(self):
        try:
            url: str = ("http://flight724.com/")
            options = webdriver.ChromeOptions()
            options.add_argument('--ignore-certificate-errors')
            options.add_argument('--incognito')
            self.driver = webdriver.Chrome(service=Service(
                "E:\Projects\sepehr_scrapper\chromedriver.exe"), options=options)
            try:
                if not self.orig_dest_are_extracted:
                    self.driver.get(url=url)
                    self.driver.find_element(By.XPATH, '//*[@id="search_auto_from"]').send_keys(self.orig + '\n')
                    self.orig_for_url = \
                        self.driver.find_element(By.XPATH, '//*[@id="search_auto_from"]').get_attribute('value').split(
                            ' ')[0]
                    self.driver.find_element(By.XPATH, '//*[@id="search_auto_to"]').send_keys(self.dest + '\n')
                    self.dest_for_url = \
                        self.driver.find_element(By.XPATH, '//*[@id="search_auto_to"]').get_attribute('value').split(
                            ' ')[0]
                    self.orig_dest_are_extracted = True
            except:
                try:
                    self.driver.close()
                except:
                    pass
                self.get_flight724_route()

            for self.day_num in range(self.day_num, self.days_num):
                flight_date = str(datetime.datetime.now() + datetime.timedelta(days=self.day_num)).split(' ')[0]
                self.driver.get(
                    url=f'http://flight724.com/Ticket-{self.orig_for_url}-{self.dest_for_url}.html?t={flight_date}')

                orig_list = []
                dest_list = []
                days_num_list = []
                price_list = []
                selling_type_list = []
                flight_num_list = []
                airline_list = []
                dep_time_list = []
                cap_list = []
                extra_info = []
                flight_class_list = []
                for n1 in range(1, len(self.driver.find_elements(By.XPATH, '//div[@class="resu "]')) + 1):
                    elem1 = self.driver.find_element(By.XPATH, f'//div[@class="resu "][{n1}]')
                    ActionChains(self.driver).move_to_element(elem1).perform()
                    orig_list.append(self.orig)
                    dest_list.append(self.dest)
                    days_num_list.append(self.days_num)
                    try:
                        price_list.append(
                            self.driver.find_element(By.XPATH, f'//*[@id="tab_record"]/div[{n1}]/div[1]/span').text)
                    except:
                        price_list.append(None)

                    try:
                        selling_type_list.append(
                            self.driver.find_element(By.XPATH,
                                                     f'//div[@class="resu "][{n1}]/div[1]/div').text)
                    except:
                        selling_type_list.append(None)

                    try:
                        flight_num_list.append(
                            self.driver.find_element(By.XPATH,
                                                     f'//div[@class="resu "][{n1}]/div[@class="code"]/span').text)
                    except:
                        flight_num_list.append(None)
                    try:
                        dep_time_list.append(
                            self.driver.find_element(By.XPATH, f'//div[@class="resu "][{n1}]/div[@class="date"]').text)
                    except:
                        dep_time_list.append(None)

                    try:
                        cap_list.append(
                            self.driver.find_element(By.XPATH, f'//div[@class="resu "][{n1}]/div[@class="user"]').text)
                    except:
                        cap_list.append(None)

                    try:
                        elem11 = self.driver.find_element(By.XPATH, f'//div[@class="resu "][{n1}]/div[@class="code"]')
                        ActionChains(self.driver).move_to_element(elem11).perform()
                        WebDriverWait(self.driver, 10).until(
                            EC.presence_of_element_located(
                                (By.XPATH, f'//div[@class="resu "][{n1}]/div[@class="code"]')))
                        airline_list.append(self.driver.find_element(By.XPATH,
                                                                     f'//div[@class="resu "][{n1}]/div[4]/div[1]/div[2]/div[2]/strong[2]').text)
                    except:
                        airline_list.append(None)
                    try:
                        extra_info.append(self.driver.find_element(By.XPATH,
                                                                   f'//div[@class="resu "][{n1}]/div[4]/div[1]/div[2]/div[3]').text.split(
                            '\n'))
                    except:
                        extra_info.append(None)

                    try:
                        flight_class_list.append(self.driver.find_element(By.XPATH,
                                                                          f'//div[@class="resu "][{n1}]/div[4]/div[1]/div[2]/div[4]').text.split(
                            '\n')[0].split(":")[1])
                    except:
                        flight_class_list.append(None)
                    elem11 = self.driver.find_element(By.XPATH, f'//div[@class="resu "]')
                    ActionChains(self.driver).move_to_element(elem11).perform()

                df = pd.DataFrame({
                    'orig': orig_list,
                    'dest': dest_list,
                    'dur': days_num_list,
                    'ticket_class': selling_type_list,
                    'flight_date': [flight_date] * len(extra_info),
                    'price': price_list,
                    'flight_num': flight_num_list,
                    'dep_time': dep_time_list,
                    'capacity': cap_list,
                    'airline': airline_list,
                    'flight_class': flight_class_list,
                    'extra_info': extra_info,
                    'scrap_date': [str(datetime.datetime.now())] * len(extra_info)
                })

                result_dict = df.to_dict('records')

                MONGODB_HOST = '192.168.115.17'
                MONGODB_PORT = 24048
                MONGODB_USER = 'kanan'
                MONGODB_PASS = '123456'
                MONGODB_DB = 'flight724_DB'
                client = MongoClient(MONGODB_HOST, MONGODB_PORT,
                                     username=MONGODB_USER,
                                     password=MONGODB_PASS,
                                     authSource=MONGODB_DB)

                db = client['flight724_DB']
                collection = db['flight724']
                if result_dict:
                    collection.insert_many(result_dict)
                self.day_num += 1
            self.driver.close()
            return True
        except Exception as e:
            try:
                self.driver.close()
            except:
                pass
            self.error_exit = 1
            return False


f_scrapper = Flight724Scrapper('THR', 'MHD', 3)
f_scrapper.get_flight724_route()
