from pymongo import MongoClient
import pandas as pd

# Replace with your actual connection details
MONGODB_HOST = '192.168.115.17'
MONGODB_PORT = 24048
MONGODB_USER = 'kanan'
MONGODB_PASS = '123456'
MONGODB_DB = 'fids_DB'
client = MongoClient(MONGODB_HOST, MONGODB_PORT,
                     username=MONGODB_USER,
                     password=MONGODB_PASS,
                     authSource=MONGODB_DB)
# Get the database and collection of MongoDB
db = client['fids_DB']
collection = db['fids2']

# Read all data from the collection
cursor = collection.find({})  # Find all documents (empty filter)

# Create an empty list to store data
data = []

# Loop through the cursor and add documents to the list
for document in cursor:
    data.append(document)

# Close the cursor to release resources
cursor.close()

# Create the DataFrame from the list of documents
df = pd.DataFrame(data)

# Print the DataFrame (optional)
print(df)

# Close the connection to MongoDB (optional)
client.close()
