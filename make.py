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

    try:
        int(age)
    except:
        return "나이는 숫자(정수)로 입력해 주세요!"
    try:
        float(bmi)
    except:
        return "bmi는 숫자(정수 또는 소수)로 입력해 주세요!"
    try:
        int(children)
    except:
        return "자녀수는 숫자(정수)로 입력해 주세요!"

  
    if (sex != 'male') & (sex != 'female'):
        return "성별은 male 또는 female 형식으로 입력해 주세요!"
    elif (smoker != 'yes') & (smoker != 'no'):
        return "흡연여부는 yes 또는 no 형식으로 입력해 주세요!"


    user_data = [[age, sex, bmi, children, smoker]]
    user_data = pd.DataFrame(user_data, columns=['age', 'sex', 'bmi', 'children', 'smoker'])
    result = pipe.predict(user_data)[0]


    return  f'당신의 연간 예상 건강보험료는 {int(result)}(달러) 입니다.'

@app.route('/bmi/<tall>/<weight>')
def get_bmi(tall, weight): # 입력값에 따른 bmi수치 출력

    try:
        int(tall)
    except:
        return "키는 숫자(정수) 형식으로 입력해 주세요!"
    try:
        int(weight)
    except:
        return "뭄무게는 숫자(정수) 형식으로 입력해 주세요!"

    
    my_bmi = round(int(weight)/((int(tall)/100)**2), 2)
    return f'당신의 bmi 수치는 {my_bmi} 입니다.'

if __name__ == "__main__":
    app.run(debug=True)