import logging
import os

from flask import Flask, request
from flask_cors import CORS

import psycopg2
import psycopg2.extras
import requests


AIRFLOW_ENDPOINT_URL = "http://airflow-webserver:8080/api/v1"
airflow_api_params = {
    'headers': {
        'Content-type': 'application/json',
        'Accept': 'application/json'
    },
    'auth': requests.auth.HTTPBasicAuth(
        os.getenv('_AIRFLOW_WWW_USER_USERNAME'),
        os.getenv('_AIRFLOW_WWW_USER_PASSWORD')
    )
}

def create_app():
    app = Flask(__name__)
    CORS(app)


    @app.route("/")
    def hello():
        return "Hello, World!"
    
    @app.route("/trigger", methods=['GET'])
    def trigger_dag():
        try:
            resp = requests.post(
                f"{AIRFLOW_ENDPOINT_URL}/dags/process_sensor_data/dagRuns",
                json={'conf': {}},
                **airflow_api_params
            )
            print(repr(resp.json()))
        except:
            logging.exception('Unable to trigger DAG!')
            return {'status': 'failed'}, 500
        return {"status": "success"}

    @app.route('/get-current-data', methods=['GET'])
    def get_current_data():
        pg_user = os.getenv('POSTGRES_USER')
        pg_pw = os.getenv('POSTGRES_PASSWORD')
        db = os.getenv('SENSOR_DATA_DB')
        conn = psycopg2.connect(
            user=pg_user,
            password=pg_pw,
            host="postgres",
            dbname=db
        )
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute('SELECT * FROM sensor_data');
        results = [ row for row in cur ]
        return results
        
    return app
    
app = create_app()