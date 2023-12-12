import datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.proxy import Proxy, ProxyType



class Flight724Scrapper:
    def __init__(self, orig, dest, days_num):
        self.orig = orig
        self.dest = dest
        self.days_num = days_num
        self.day_num_text = None
        self.day_num = 0
        self.error_exit = 0

    def get_flight724_route(self):
        try:
            url: str = ("http://flight724.com/")
            options = webdriver.ChromeOptions()
            options.add_argument('--ignore-certificate-errors')
            options.add_argument('--incognito')
            PROXY = "127.0.0.1:65386"
            # options.add_argument('--proxy-server=%s' % PROXY)
            options.add_extension('C:/Users\Administrator\Desktop\Projects\sepehr_fids_scrapper\sepehr_scrapper/majdfhpaihoncoakbjgbdhglocklcgno.crx')
            driver = webdriver.Chrome(service=Service(
                "C:/Users\Administrator\Desktop\Projects\sepehr_fids_scrapper/chromedriver.exe"), options=options)
            try:
                driver.get(url=url)
            except:
                try:
                    driver.close()
                except:
                    pass
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
            else:
                driver.find_element(By.XPATH,
                                    '//a[contains(@class, "weekday") and not(contains(@class, "invalid"))]').click()
            driver.find_element(By.XPATH, '//*[@id="search_submit"]').click()

            for self.day_num in range(self.day_num, self.days_num):
                if self.day_num > 0 and not self.error_exit:
                    WebDriverWait(driver, 3).until(
                        EC.presence_of_element_located((By.XPATH, '//a[contains(text(), "روز بعد")]')))
                    driver.find_element(By.XPATH, '//a[contains(text(), "روز بعد")]').click()
                try:
                    self.error_exit = 0
                    WebDriverWait(driver, 3).until(
                        EC.presence_of_element_located(
                            (By.XPATH, f'//div[@class="resu "]')))
                except:
                    if driver.find_element(By.XPATH, '//*[@id="fromprice"]/div[2]/div[1]').text == '0 تا ( نتیجه)':
                        continue
                    else:
                        raise 1

                self.day_num_text = driver.find_element(By.XPATH, '//*[@id="r_city_date"]/span').text

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
                flight_date = driver.find_element(By.XPATH, '//*[@id="r_city_date"]/span').text
                for n1 in range(1, len(driver.find_elements(By.XPATH, '//div[@class="resu "]')) + 1):
                    elem1 = driver.find_element(By.XPATH, f'//div[@class="resu "][{n1}]')
                    ActionChains(driver).move_to_element(elem1).perform()
                    orig_list.append(self.orig)
                    dest_list.append(self.dest)
                    days_num_list.append(self.days_num)
                    try:
                        price_list.append(
                            driver.find_element(By.XPATH, f'//div[@class="resu "][{n1}]/div[@class="price"]/span').text)
                    except:
                        price_list.append(None)

                    try:
                        class_icon_list.append(
                            driver.find_element(By.XPATH,
                                                f'//div[@class="resu "][{n1}]/div[1]/div').text)
                    except:
                        class_icon_list.append(None)

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
                    'dur': days_num_list,
                    'class': class_icon_list,
                    'flight_date': [flight_date] * len(extra_info),
                    'price': price_list,
                    'type': type_list,
                    'datetime': datetime_list,
                    'capacity': cap_list,
                    'airline': airline_list,
                    'airplane_class': class_list,
                    'extra_info': extra_info,
                    'scrap_date': [str(datetime.datetime.now())] * len(extra_info)
                })

                result_dict = df.to_dict('records')

                # Connect to the MongoDB server
                MONGODB_HOST = '192.168.115.17'
                MONGODB_PORT = 24048
                MONGODB_USER = 'kanan'
                MONGODB_PASS = '123456'
                MONGODB_DB = 'flight724_DB'
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

                # sql_server = '192.168.40.57'
                # sql_database = 'fids_mongodb'
                # sql_username = 'k.sehat'
                # sql_password = 'K@123456'
                # cnxn = pyodbc.connect(driver='{SQL Server}',
                #                       server=sql_server,
                #                       database=sql_database,
                #                       uid=sql_username, pwd=sql_password)
                # cursor = cnxn.cursor()
                # insert_stmt = "INSERT INTO FIDS_JSON (jsoncontent,SiteName) VALUES (?,?)"
                # cursor.execute(insert_stmt, (str(df.to_dict()), '724'))
                # cnxn.commit()
                # cnxn.close()
            driver.close()
            return True
        except Exception as e:
            try:
                driver.close()
            except:
                pass
            self.error_exit = 1
            return False


# f_scrapper = Flight724Scrapper('THR', 'MHD', 1)
# trampoline(f_scrapper.get_flight724_route)
