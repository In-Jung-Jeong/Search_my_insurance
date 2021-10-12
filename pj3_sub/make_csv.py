from pymongo import MongoClient
import json
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from category_encoders import OrdinalEncoder
from xgboost import XGBRegressor

import os
from flask import Flask, jsonify, render_template

# mongodb 데이터 불러오기
HOST = 'cluster0.x1l7v.mongodb.net'
USER = 'codeking'
PASSWORD = 'codeking1234'
DATABASE_NAME = 'myFirstDatabase'
COLLECTION_NAME = 'project3'
MONGO_URI = f"mongodb+srv://{USER}:{PASSWORD}@{HOST}/{DATABASE_NAME}?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE"

client = MongoClient(MONGO_URI)

database = client[DATABASE_NAME]

collection = database[COLLECTION_NAME]

csv_file = collection.find_one()
df = pd.DataFrame(csv_file)

df = df.drop('region', axis=1)
df = df.drop('_id', axis=1)

enc = OrdinalEncoder()
df = enc.fit_transform(df)

df = df.corr()
df = df[5:]
df.to_csv('dsboard_2.csv', index=False)