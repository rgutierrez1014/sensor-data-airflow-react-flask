import csv
from datetime import timedelta

import airflow
from airflow import DAG

from tasks import setup_db, process_data


default_args = {
    'start_date': airflow.utils.dates.days_ago(0),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}


dag = DAG(
    'process_sensor_data',
    default_args=default_args,
    description='example dag that takes sample sensor data, calculates mean, median, and standard deviation, and saves to Postgres db',
    schedule_interval=None,
    dagrun_timeout=timedelta(minutes=20)
)


t1 = setup_db(dag)
t2 = process_data(dag)

t1 >> t2
