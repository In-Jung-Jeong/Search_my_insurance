from pymongo import MongoClient
import json
import pandas as pd
import pickle

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


# 모델링 시작
df = df.drop('region', axis=1)
df = df.drop('_id', axis=1)

target = 'charges'
features = df.drop(target, axis=1).columns
train, test = train_test_split(df, train_size=0.80, test_size=0.20,
                              random_state=2)
train, val = train_test_split(train, train_size=0.80, test_size=0.20,
                              random_state=2)

X_train = train[features]
X_val = val[features]
X_test = test[features]

y_train = train[target]
y_val = val[target]
y_test = test[target]

pipe = make_pipeline(
    OrdinalEncoder(),
    XGBRegressor(max_depth=5, n_estimators = 50, random_state=2)
)

pipe.fit(X_train, y_train)

with open('model.pkl', 'wb') as model_file:
  pickle.dump(pipe, model_file)