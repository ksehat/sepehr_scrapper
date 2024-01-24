import datetime
import time
import numpy as np
import requests
import json
import pandas as pd
import concurrent.futures
import threading


def process_df(process_dict):

        while True:
            with concurrent.futures.ThreadPoolExecutor(max_workers=process_dict['num_of_workers']) as executor:
                list(executor.map(runner, process_dict['df'].itertuples(index=False)))
            print(f'the {process_dict["df"]} is done and im going to sleep {process_dict["interval"]}')
            time.sleep(process_dict['interval'] * 3600)


def runner(data):
    try:
        r = requests.post(url='http://192.168.115.17:3000/scrap_runner', json=json.dumps(list(data)))
        print(list(data), datetime.datetime.now(), r)
    except:
        runner(data)

def num_of_workers_for_group(interval):
    # if interval <= 2:
    #     return 5
    # if  interval > 2 and interval<:
    #     return 5
    # else:
    return 5


scrap_data = pd.read_csv('E:\Projects\sepehr_scrapper\source for scrap/ROUT.csv')
# TODO: after implementation of alibaba and flytoday scrapers this line should be deleted
scrap_data = scrap_data[scrap_data['site']=='alameer.ir']

scrap_data['per_hour'] = 24/scrap_data['perday']

data_dict = {}
for interval in scrap_data['per_hour'].unique():
    data_dict[interval] = {}
    data_dict[interval]['df'] = scrap_data[scrap_data['per_hour'] == interval]
    data_dict[interval]['num_of_workers'] = num_of_workers_for_group(interval)
    data_dict[interval]['interval'] = interval

threads = []
for k in data_dict.keys():
    t = threading.Thread(target=process_df, args=[data_dict[k]])
    t.start()
    threads.append(t)

# Join the threads using a for loop
for t in threads:
    t.join()