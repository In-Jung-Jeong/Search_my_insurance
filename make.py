from pymongo import MongoClient
import json
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from category_encoders import OrdinalEncoder
from xgboost import XGBRegressor

import os
from flask import Flask, jsonify, render_template
import pickle

with open("model.pkl","rb") as fr:
    pipe = pickle.load(fr)

# flask 앱 제작
app = Flask(__name__)

@app.route("/")
def get_main(): # 메인화면 출력
    return render_template('main.html')

@app.route('/<age>/<sex>/<bmi>/<children>/<smoker>')
def get_charges(age, sex, bmi, children, smoker): # 입력값에 따른 연간 예상 건강보험료 출력


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