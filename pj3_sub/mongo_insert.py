from pymongo import MongoClient
import pandas as pd
import json

# 로컬 환경에 있는 csv파일 mongodb에 업로드 하기.
test = pd.read_csv('insurance.csv')

dbdata = test.to_json()
dbdata = json.loads(dbdata)

HOST = 'cluster0.x1l7v.mongodb.net'
USER = 'codeking'
PASSWORD = 'codeking1234'
DATABASE_NAME = 'myFirstDatabase'
COLLECTION_NAME = 'project3'
MONGO_URI = f"mongodb+srv://{USER}:{PASSWORD}@{HOST}/{DATABASE_NAME}?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE"

# mongodb+srv://codeking:<password>@cluster0.x1l7v.mongodb.net/myFirstDatabase?retryWrites=true&w=majority

client = MongoClient(MONGO_URI)

database = client[DATABASE_NAME]

collection = database[COLLECTION_NAME]

collection.insert_one(dbdata)