import logging
import os

from flask import Flask, request
from flask_cors import CORS

import psycopg2
import psycopg2.extras
import psycopg2.extensions
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


def response_fail(msg, code=500):
    """
    Uniform way to return a "failed" response as JSON
    """
    return {'status': 'failed', 'message': msg}, code


def fail_from_error(msg):
    """
    Streamline code for returning a failed response from within 
    an `except` statement
    """
    logging.exception(msg)
    return response_fail(msg)


def create_app():
    app = Flask(__name__)
    CORS(app)


    @app.route("/")
    def hello():
        return "Hello, World!"
    
    @app.route("/trigger", methods=['GET'])
    def trigger_dag():
        """
        Trigger a DAG run. Un-pause the DAG first in case it is 
        paused.
        """
        try:
            resp = requests.patch(
                f"{AIRFLOW_ENDPOINT_URL}/dags/process_sensor_data",
                json={'is_paused': False},
                **airflow_api_params
            )
            print(repr(resp.json()))
        except:
            return fail_from_error('Unable to un-pause DAG!')
        try:
            resp = requests.post(
                f"{AIRFLOW_ENDPOINT_URL}/dags/process_sensor_data/dagRuns",
                json={'conf': {}},
                **airflow_api_params
            )
        except:
            return fail_from_error('Unable to trigger DAG!')
        return {"status": "success"}

    @app.route('/get-current-data', methods=['GET'])
    def get_current_data():
        """
        Query DB table for full data
        """
        pg_user = os.getenv('POSTGRES_USER')
        pg_pw = os.getenv('POSTGRES_PASSWORD')
        db = os.getenv('SENSOR_DATA_DB')
        try:
            conn = psycopg2.connect(
                user=pg_user,
                password=pg_pw,
                host="postgres",
                dbname=db
            )
        except psycopg2.Error as e:
            if 'does not exist' in str(e):
                msg = "Database might not exist yet. Wait a few moments and try again."
            else:
                msg = "Connection error"
            return fail_from_error(msg)
        except:
            logging.exception('Unknown failure')
            return {'status': 'failed'}, 500
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute('SELECT * FROM sensor_data');
        results = [ row for row in cur ]
        return {'status': 'success', 'data': results}
        
    return app
    
app = create_app()