from pymongo import MongoClient
from datetime import datetime


def flight724_mongo_cleaner():
    # Connect to MongoDB
    MONGODB_HOST = '192.168.115.17'
    MONGODB_PORT = 27017
    MONGODB_USER = 'kanan'
    MONGODB_PASS = '123456'
    MONGODB_DB = 'fids_DB'
    client = MongoClient(MONGODB_HOST, MONGODB_PORT,
                         username=MONGODB_USER,
                         password=MONGODB_PASS,
                         authSource=MONGODB_DB)
    db = client['flight724_DB']
    flight724 = db['flight724']
    flight724_cleaned = db['flight724_cleaned']

    # Sort data by scrape_date
    data = list(flight724.find().sort('scrape_date', 1))

    # Remove consecutive redundant documents
    fields_to_ignore = ['_id', 'scrape_date', 'price', 'capacity', 'extra_info']
    cleaned_data = []

    for i in range(len(data)):
        if i == 0 or any(data[i][field] not in [d[field] for d in cleaned_data] for field in data[i] if
                         field not in fields_to_ignore):
            cleaned_data.append(data[i])

    # Append cleaned data to flight724_cleaned collection
    if cleaned_data:
        flight724_cleaned.insert_many(cleaned_data)

    # Remove all data from flight724 collection
    flight724.delete_many({})
