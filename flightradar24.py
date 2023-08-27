import copy
import datetime
import random
import threading
import requests
import json
import time
from pymongo import MongoClient


def insert_update_DB(result_dict, airport, page_num):
    # Connect to the MongoDB server
    MONGODB_HOST = '192.168.115.17'
    MONGODB_PORT = 27017
    MONGODB_USER = 'kanan'
    MONGODB_PASS = '123456'
    MONGODB_DB = 'flightradar24_DB'
    client = MongoClient(MONGODB_HOST, MONGODB_PORT,
                         username=MONGODB_USER,
                         password=MONGODB_PASS,
                         authSource=MONGODB_DB)
    db = client['flightradar24_DB']
    collection = db['flightradar24']

    last_existing_doc = collection.find_one({'airport': airport, 'page': page_num}, sort=[('insert_date', -1)])
    if last_existing_doc:
        last_existing_date = last_existing_doc['insert_date']
        if datetime.datetime.now().date() == last_existing_date.date():
            collection.find_one_and_replace({'_id': last_existing_doc['_id']}, result_dict, upsert=True)
        else:
            collection.insert_one(result_dict)
    else:
        collection.insert_one(result_dict)


class get_flightradar24:
    def __init__(self, airport):
        self.page_num = 1
        self.total_pages = 1
        self.airport = airport

    def scrapper(self):
        try:
            url = f"https://api.flightradar24.com/common/v1/airport.json?code={self.airport}&page={self.page_num}"
            payload = {}
            headers = {
                'authority': 'api.flightradar24.com',
                'accept': 'application/json, text/plain, */*',
                'accept-language': 'en-US,en;q=0.9',
                'origin': 'https://www.flightradar24.com',
                'referer': 'https://www.flightradar24.com/',
                'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-site',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
                'Cookie': '__cfruid=8dccc46d48bf9b56b2a123c4446b55ed23228bf5-1692510945'
            }
            try:
                response = requests.request("GET", url, headers=headers, data=payload)
            except Exception as e:
                print(f'{e}')
                print(f'Error occured at {datetime.datetime.now()}')
                return True
            try:
                result = json.loads(response.text)
            except:
                return True

            if self.page_num == 1:
                self.total_pages = max(
                    result['result']['response']['airport']['pluginData']['schedule']['arrivals']['page']['total'],
                    result['result']['response']['airport']['pluginData']['schedule']['departures']['page'][
                        'total'],
                    result['result']['response']['airport']['pluginData']['schedule']['ground']['page']['total'])


            result_dict = {}
            result_dict['result'] = result['result']['response']['airport']
            result_dict['airport'] = self.airport
            result_dict['page'] = self.page_num
            result_dict['insert_date'] = datetime.datetime.now()
            try:
                insert_update_DB(result_dict, self.airport, self.page_num)
                if self.page_num <= self.total_pages:
                    self.page_num += 1
            except:
                print('Data is not inserted/updated in MongoDB.')
                return True
        except Exception as e:
            print(e)
            print(
                'Error in the json decoder. Maybe the request was not okay and the results of the request was null')
            return True

    def runner_and_page_controller(self):
        while self.page_num <= self.total_pages:
            self.scrapper()


def worker(airport):
    while True:
        get_flightradar24(airport).runner_and_page_controller()
        time.sleep(random.randint(30, 60))


airport_list = ['ika', 'thr', 'mhd', 'syz', 'kih']
threads = []
for airport in airport_list:
    t = threading.Thread(target=worker, args=(airport,))
    t.start()
    threads.append(t)
    # worker(airport)

for t in threads:
    t.join()
