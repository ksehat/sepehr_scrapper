import time

import requests
import json
import pandas as pd
import concurrent.futures
import threading


def process_df(df, num_workers):
    while True:
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
            list(executor.map(runner, df.itertuples(index=False)))



def runner(data):
    print(data)
    r = requests.post(url='http://192.168.115.17:3000/flight724', json=json.dumps(list(data)))


scrap_data = pd.read_excel('C:/Users\Administrator\Desktop\Projects/Flight724_Sc.xlsx')
dur_cols = [col for col in scrap_data.columns if col.startswith('dur')]

# Create a dictionary to store the new dataframes
dfs = {}

# Iterate over the 'dur' columns
for col in dur_cols:
    # Create a new dataframe with the first two columns and the current 'dur' column
    dfs[f'df_{col}'] = scrap_data[['orig', 'dest', col]]

# Create a list of arguments for each thread

thread_args = [
    (dfs['df_dur4'], 7),
    (dfs['df_dur3'], 3),
    (dfs['df_dur2'], 1),
    (dfs['df_dur1'], 1)
]

# Create and start the threads using a for loop
threads = []
for args in thread_args:
    t = threading.Thread(target=process_df, args=args)
    t.start()
    threads.append(t)

# Join the threads using a for loop
for t in threads:
    t.join()
