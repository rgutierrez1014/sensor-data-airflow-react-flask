import csv
from datetime import timedelta

import airflow
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

import datadotworld as dw
import requests


"""
TASKS
"""

def do_something_fn():
    """
    Do something
    """
    with dw.open_remote_file('r-a-gutierrez/sensor-data-test', 'argentine-zones-north-winds-stats.csv', mode='r') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            if i == 5:
                break
            print(row)


def do_something(dag):
    return PythonOperator(
        task_id="do_something",
        python_callable=do_something_fn,
        dag=dag
    )


def do_something_again_fn():
    """
    Do something
    """
    return 'hello world, again!'


def do_something_again(dag):
    return PythonOperator(
        task_id="do_something_again",
        python_callable=do_something_again_fn,
        dag=dag
    )


"""
DAG
"""

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
    dagrun_timeout=timedelta(minutes=20))


t1 = do_something(dag)
t2 = do_something_again(dag)

t1 >> t2
