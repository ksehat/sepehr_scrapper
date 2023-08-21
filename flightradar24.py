import datetime
import random
import threading
import requests
import json
import time
from pymongo import MongoClient


def job(airport):
    url = f"https://api.flightradar24.com/common/v1/airport.json?code={airport}"

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
        pass
    result = json.loads(response.text)

    result_dict = result['result']['response']['airport']['pluginData']['schedule']

    result_dict['airport'] = airport
    result_dict['insert_date'] = datetime.datetime.now()

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

    # Get the database and collection
    db = client['flightradar24_DB']
    collection = db['flightradar24']
    # Insert a document
    try:
        collection.insert_one(result_dict)
    except:
        print(f'Error. Data was not inserted to the DB.')
        pass


def worker(airport):
    while True:
        job(airport)
        time.sleep(random.randint(30, 60))

airport_list = ['ika','thr','mhd','syz','kih']
threads = []
for airport in airport_list:
    t = threading.Thread(target=worker, args=(airport,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()
