import unittest
import pickle
import pandas as pd
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

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

def getResponse(body):
    try:
        missingCols = []
        requiredColumns = ['weight', 'height', 'email', 'soda', 'fast_food', 'self', 'exercise']
        for i in requiredColumns:
            if i not in body.keys():
                missingCols.append(i) 
        
        if len(missingCols) > 0:
            return f'ERROR - missing required columns: {missingCols}', 400

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
        
        return {
                'is_possible_user': is_possible_user[0],
                'score': is_possible_user[1]
            }

    except Exception as ex:
        return {'error': 'error'}

class TestConnections(unittest.TestCase):
    def test_database(self):
        try:
            cnxn = psycopg2.connect(
                host=os.getenv('DB_HOST'),
                database=os.getenv('DB_DATABASE'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PWD'),
                port=os.getenv('DB_PORT')
            )
            self.assertIsNotNone(cnxn)
            cnxn.close()
            print("✔️  SQL database connection success!")
        except Exception as e:
            self.fail(f"❌  Failed to connect to SQL database: {e}")

    def test_post_submit_response_true(self):
        body = {
            "weight": 50,
            "height": 1.68,
            "email": "teste@email.com",
            "exercise": 40,
            "self": 1,
            "fast_food": 1,
            "soda": 0
        }
        response = getResponse(body)
        
        self.assertEqual(response, {
            "is_possible_user": True,
            "score": 4
        })  

    def test_post_submit_response_false(self):
        body = {
            "weight": 100,
            "height": 1.68,
            "email": "teste@email.com",
            "exercise": 4,
            "self": 4,
            "fast_food": 5,
            "soda": 2
        }
        response = getResponse(body)
        
        self.assertEqual(response, {
            "is_possible_user": False,
            "score": -4
        }) 
        
    def test_post_missing_columns(self):
        body = {
            "weight": "WEIGHT",
            "height": 1.68,
            "email": "teste@email.com",
            "exercise": 4,
            "self": 4,
            "fast_food": 5,
            "soda": 2
        }
        response = getResponse(body)
        
        self.assertEqual(response, {
            "error": "error"
        })  
        
    def test_post_missing_columns(self):
        body = {
            "weight": 120,
            "height": 1.68,
            "email": "teste@email.com"
        }
        response = getResponse(body)
        
        self.assertEqual(response, {
            "error": "ERROR - missing required columns: ['soda', 'fast_food', 'self', 'exercise']"
        })  
if __name__ == "__main__":
    unittest.main()