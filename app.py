from flask import Flask, request, jsonify
import pickle
import pandas as pd
import psycopg2
from dotenv import load_dotenv
from psycopg2 import OperationalError
import os

load_dotenv()

app = Flask(__name__)

def connect() -> psycopg2.extensions.connection:
    try:
        cnxn = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_DATABASE'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PWD'),
            port=int(os.getenv('DB_PORT'))
        )
        
        return cnxn
    except OperationalError as oe:
        return None

def disconnect(cnxn):
    if cnxn:
        cnxn.close()

def calculate_possible_user(response_obesity, response_habits):
    weight_obesity = {
        "Insufficient Weight": 2,
        "Normal Weight": 3,
        "Overweight Level I": 1,
        "Overweight Level II": -1,
        "Obesity Type I": -2,
        "Obesity Type II": -3,
        "Obesity Type III": -4
    }
 
    weight_habits = {
        1: 4,
        4: 1,
        2: 0,
        3: -4,
        0: -4  
    }
 
    score = weight_obesity.get(response_obesity, 0) + weight_habits.get(response_habits, 0)
    is_possible_user = score >= 0
   
    return is_possible_user, score


@app.route('/getResponse/', methods=['POST'])
def getResponse():
    try:
        body = request.get_json()

        missingCols = []
        requiredColumns = ['weight', 'height', 'email', 'soda', 'fast_food', 'self', 'exercise']
        for i in requiredColumns:
            if i not in body.keys():
                missingCols.append(i) 
        
        if len(missingCols) > 0:
            return jsonify({'error':f'ERROR - missing required columns: {missingCols}'}), 400

        model_obesity = pickle.load(open('model_obesity.pkl','rb'))
        
        vals = [body['height'], body['weight']]
        cols = ['Height', 'Weight']
        
        test = {}
        for i in range(0,len(vals)):
            test[cols[i]] = vals[i]
        
        data = pd.DataFrame([test])
        response_obesity = model_obesity.predict(data)[0]
        
        
        model_habits = pickle.load(open('model_habits.pkl','rb'))
        
        vals = [body['exercise'], body['self'], body['fast_food'], body['soda'], body['weight'], body['height']]
        cols = ['euexfreq', 'eugenhth', 'eufastfdfrq', 'eudietsoda', 'euwgt', 'euhgt']
        
        test = {}
        for i in range(0,len(vals)):
            test[cols[i]] = vals[i]
        
        test = pd.DataFrame([test])
        response_habits = int(model_habits.predict(test)[0])
        
        is_possible_user = calculate_possible_user(response_obesity, response_habits)
        
        cnxn = connect()
        cursor = cnxn.cursor()
        
        cursor.execute(f"INSERT INTO let_ia_responses(email, weight, height, exercise, self, fast_food, soda, response_obesity, response_habits, is_possible_user, score) VALUES ('{body['email']}', {float(body['weight'])}, {float(body['height'])}, {int(body['exercise'])}, {int(body['self'])}, {int(body['fast_food'])}, {int(body['soda'])},'{str(response_obesity)}', {response_habits}, {is_possible_user[0]}, {is_possible_user[1]})")

        cnxn.commit()
        cursor.close()
        disconnect(cnxn)

        return jsonify(
            {
                'is_possible_user': is_possible_user[0],
                'score': is_possible_user[1]
            }
        ), 200
        
    except Exception as ex:
        try:
            disconnect(cnxn)
        except:
            pass
        return jsonify({'error': 'error'}), 500
    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
