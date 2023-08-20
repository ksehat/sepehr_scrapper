import time
from pymongo import MongoClient
import schedule
from bson.objectid import ObjectId


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
    cleaned_data = list(flight724_cleaned.find().sort('scrape_date', 1))

    # Remove consecutive redundant documents
    fields_to_ignore = ['_id', 'scrap_date', 'price', 'capacity', 'airplane_class']
    compare_fields = ['price', 'capacity', 'airplane_class']
    ids_to_remove = []
    for i in range(len(data)):
        ids_to_remove.append(data[i]['_id'])
        same_fields = [field for field in list(data[i].keys()) if field not in fields_to_ignore]
        if len(cleaned_data) != 0:
            for j in range(len(cleaned_data) - 1, -1, -1):
                if all(data[i][field1] == cleaned_data[j][field1] for field1 in same_fields):
                    if any(data[i][field] != cleaned_data[j][field] for field in compare_fields):
                        # data[i]['_id'] = ObjectId(data[i]['_id'].binary + b' cleaned')
                        cleaned_data.append(data[i])
                        flight724_cleaned.insert_one(data[i])
                        break
                    else:
                        break
                elif j == 0:
                    # data[i]['_id'] = ObjectId(data[i]['_id'].binary + b' cleaned')
                    cleaned_data.append(data[i])
                    flight724_cleaned.insert_one(data[i])
        else:
            # data[i]['_id'] = ObjectId(data[i]['_id'].binary + b' cleaned')
            cleaned_data.append(data[i])
            flight724_cleaned.insert_one(data[i])

    # flight724.delete_many({'_id': {'$in': ids_to_remove}})

flight724_mongo_cleaner()
schedule.every(10).minutes.do(flight724_mongo_cleaner)
while True:
    schedule.run_pending()
    time.sleep(1)
