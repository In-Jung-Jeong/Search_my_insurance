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


# flask 앱 제작
app = Flask(__name__)

@app.route("/")
def get_main(): # 메인화면 출력
    return render_template('main.html')

@app.route('/<age>/<sex>/<bmi>/<children>/<smoker>')
def get_charges(age, sex, bmi, children, smoker): # 입력값에 따른 연간 예상 건강보험료 출력

    test = str(df['age'][0])

    user_data = [[age, sex, bmi, children, smoker]]
    user_data = pd.DataFrame(user_data, columns=['age', 'sex', 'bmi', 'children', 'smoker'])
    result = pipe.predict(user_data)[0]


    return  f'당신의 연간 예상 건강보험료는 {int(result)}(달러) 입니다.'

@app.route('/bmi/<tall>/<weight>')
def get_bmi(tall, weight): # 입력값에 따른 bmi수치 출력
    my_bmi = round(int(weight)/((int(tall)/100)**2), 2)
    return f'당신의 bmi 수치는 {my_bmi} 입니다.'

if __name__ == "__main__":
    app.run(debug=True)