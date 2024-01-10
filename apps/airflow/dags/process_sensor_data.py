from datetime import timedelta

import airflow
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

import requests


data_world_token = "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJweXRob246ci1hLWd1dGllcnJleiIsImlzcyI6ImNsaWVudDpweXRob246YWdlbnQ6ci1hLWd1dGllcnJlejo6ODg5NmFiNDctOWU2OC00YzlmLThmNDAtMTVmMDNmZDRmZjZmIiwiaWF0IjoxNzA0NzU4NTE5LCJyb2xlIjpbInVzZXJfYXBpX2FkbWluIiwidXNlcl9hcGlfcmVhZCIsInVzZXJfYXBpX3dyaXRlIl0sImdlbmVyYWwtcHVycG9zZSI6dHJ1ZSwic2FtbCI6e319.bMOxJLGG2qJtKIZbXCt_L3nldkw7p2XCj9OXslCDSmJw7qvBJ4p2Nrs-_rH-b4L7ApsnBSPhbwBpHBC8-8MmuA"


"""
TASKS
"""

def do_something_fn():
    """
    Do something
    """
    return 'hello world!'


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
