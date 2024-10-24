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


@app.route('/getResponse/', methods=['POST'])
def getResponse():
    try:
        body = request.get_json()

        missingCols = []
        if 'weight' not in body.keys():
            missingCols.append('weight') 
        if 'height' not in body.keys():
            missingCols.append('height')
        if 'email' not in body.keys():
            missingCols.append('email') 

        if len(missingCols) > 0:
            return f'ERROR - missing required columns: {missingCols}', 400

        # model = pickle.load(open('model.pkl','rb'))
        # preprocessor = pickle.load(open('label-encoder.pkl','rb'))
        
        # vals = [body['height'], body['weight']]
        # cols = preprocessor.transformers_[0][2]
        
        # test = {}
        # for i in range(0,len(vals)):
        #     test[cols[i]] = vals[i]
        
        # test = pd.DataFrame([test])
        # data = preprocessor.transform(test)
        
        # response = model.predict(data)[0]
        response = True
        
        cnxn = connect()
        cursor = cnxn.cursor()
        
        cursor.execute(f"INSERT INTO let_ia_responses(email, weight, height, response) VALUES ('{body['email']}', {float(body['weight'])}, {float(body['height'])}, {response})")
         
        cnxn.commit()
        cursor.close()
        disconnect(cnxn)

        return jsonify({'response': response}), 200
    except Exception as ex:
        print(ex)
        return jsonify({'error': 'error'}), 500
    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
