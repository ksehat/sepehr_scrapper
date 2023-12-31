import datetime
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient
from selenium.webdriver.chrome.service import Service


def scroll_to_the_end(driver):
    SCROLL_PAUSE_TIME = 0.5
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


class FlightioScrapper:
    def __init__(self, orig, dest, days_num=1, flight_date=None, id_from_backend=None):
        self.orig = orig
        self.dest = dest
        self.days_num = days_num
        self.day_num = 0
        self.flight_date = flight_date
        self.id_from_backend = id_from_backend
        self.orig_dest_are_extracted = False
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument('--incognito')
        self.url = "http://flightio.com/"

    def get_flightio_route(self):
        try:
            try:
                self.driver = webdriver.Chrome(service=Service(
                    "E:\Projects\sepehr_scrapper\chromedriver.exe"), options=self.options)
            except:
                try:
                    self.driver.close()
                except:
                    pass
                self.get_flight724_route()

            for self.day_num in range(self.day_num, self.days_num):

                if self.flight_date:
                    self.driver.get(
                        url=f'https://flightio.com/flight/search/2/{self.orig}-{self.dest}/{self.flight_date}/1-0-0-1')
                else:
                    flight_date = str(datetime.datetime.now() + datetime.timedelta(days=self.day_num)).split(' ')[0]
                    self.driver.get(
                        url=f'https://flightio.com/flight/search/2/{self.orig}-{self.dest}/{flight_date}/1-0-0-1')

                orig_list = []
                dest_list = []
                days_num_list = []
                price_list = []
                selling_type_list = []
                airplane_name_list = []
                flight_num_list = []
                airline_list = []
                dep_time_list = []
                ticket_class_list = []

                scroll_to_the_end(self.driver)

                for n1 in range(1, len(self.driver.find_elements(By.XPATH,
                                                     f'//*[@id="DepartListSection"]/div/div')) + 1):
                    elem1 = self.driver.find_element(By.XPATH, f'//*[@id="DepartListSection"]/div[{n1}]/div')
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elem1)
                    orig_list.append(self.orig)
                    dest_list.append(self.dest)
                    days_num_list.append(self.days_num)
                    try:
                        price_list.append(
                            self.driver.find_element(By.XPATH,
                                                     f'//*[@id="DepartListSection"]/div[{n1}]/div/div[2]/div[3]/div[2]/button[1]').text.split(
                                ' ')[0])
                    except:
                        price_list.append(None)

                    try:
                        elem_temp = self.driver.find_elements(By.XPATH,
                                                              f'//*[@id="DepartListSection"]/div[{n1}]/div/div[1]/div/label')
                        selling_type_list.append([ali.text for ali in elem_temp])
                    except:
                        selling_type_list.append(None)

                    try:
                        dep_time_list.append(
                            self.driver.find_element(By.XPATH,
                                                     f'//*[@id="DepartListSection"]/div[{n1}]/div/div[2]/div[2]/div[2]/span[1]').text)
                    except:
                        dep_time_list.append(None)

                    try:
                        airline_list.append(self.driver.find_element(By.XPATH,
                                                                     f'//*[@id="DepartListSection"]/div[{n1}]/div/div[2]/div[1]/div[2]/span[1]').text)
                    except:
                        airline_list.append(None)

                    self.driver.find_element(By.XPATH,
                                             f'//*[@id="DepartListSection"]/div[{n1}]/div/div[1]/button').click()
                    try:
                        flight_num_list.append(
                            self.driver.find_element(By.XPATH,
                                                     f'//*[@id="DepartListSection"]/div[{n1}]/div/div[3]/div[2]/div[1]/span[2]').text)
                    except:
                        flight_num_list.append(None)
                    try:
                        ticket_class_list.append(self.driver.find_element(By.XPATH,
                                                                          f'//*[@id="DepartListSection"]/div[{n1}]/div/div[3]/div[2]/div[2]/span[2]').text)
                    except:
                        ticket_class_list.append(None)
                    try:
                        airplane_name_list.append(self.driver.find_element(By.XPATH,
                                                                           f'//*[@id="DepartListSection"]/div[{n1}]/div/div[3]/div[2]/div[4]/span[2]').text)
                    except:
                        airplane_name_list.append(None)

                df = pd.DataFrame({
                    'source': ['flight724'] * len(price_list),
                    'orig': orig_list,
                    'dest': dest_list,
                    'dur': days_num_list,
                    'ticket_selling_type': selling_type_list,
                    'flight_date': [self.flight_date if self.flight_date else flight_date] * len(price_list),
                    'price': price_list,
                    'flight_num': flight_num_list,
                    'dep_time': dep_time_list,
                    'airline': airline_list,
                    'ticket_class': ticket_class_list,
                    'airplane_model': airplane_name_list,
                    'id_from_backend': self.id_from_backend if self.id_from_backend else 'scrap',
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
                    collection = db['flightio']
                    collection.insert_many(result_dict)
                self.day_num += 1
            self.driver.close()
            return [True, df]
        except Exception as e:
            try:
                self.driver.close()
            except:
                pass
            return [False, False]


# f_scrapper = FlightioScrapper('THR', 'MHD', flight_date='2024-01-05')
# result = False
# while result == False:
#     result = f_scrapper.get_flightio_route()[0]
