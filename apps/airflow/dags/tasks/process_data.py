import csv
from datetime import datetime
from decimal import Decimal
import os
from statistics import median, mean, stdev

from airflow.operators.python_operator import PythonOperator

import datadotworld as dw
import psycopg2


def process_data_fn(**kwargs):
    """
    Grab data from data.world and calculate mean, median, and 
    standard deviation.
    """
    pg_user = os.getenv('POSTGRES_USER')
    pg_pw = os.getenv('POSTGRES_PASSWORD')
    db = os.getenv('SENSOR_DATA_DB')
    conn = psycopg2.connect(
        user=pg_user,
        password=pg_pw,
        host="postgres",
        dbname=db
    )
    conn.autocommit = True
    cur = conn.cursor()
    ufp, bc, no2 = [ [] for i in range(3) ]
    with dw.open_remote_file('r-a-gutierrez/sensor-data-test', 'argentine-zones-north-winds-stats.csv', mode='r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('Z1UFP'):
                ufp.append(Decimal(row['Z1UFP']))
            if row.get('Z1BC'):
                bc.append(Decimal(row['Z1BC']))
            if row.get('Z1NO2'):
                no2.append(Decimal(row['Z1NO2']))
    if len(ufp) == 0 or len(bc) == 0 or len(no2) == 0:
        raise Exception('One or more fields was not computed properly!')
    ufp_values = [ fn(ufp) for fn in (mean, median, stdev) ]
    bc_values = [ fn(bc) for fn in (mean, median, stdev) ]
    no2_values = [ fn(no2) for fn in (mean, median, stdev) ]
    query_params = [kwargs['run_id']] + ufp_values + bc_values + no2_values + [datetime.utcnow()]
    query = """INSERT INTO sensor_data (
        run_id,
        ufp_mean,
        ufp_median,
        ufp_stddev,
        bc_mean,
        bc_median,
        bc_stddev,
        no2_mean,
        no2_median,
        no2_stddev,
        created_at
    ) VALUES (
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s
    )"""
    cur.execute(query, query_params)
    conn.close()


def process_data(dag):
    return PythonOperator(
        task_id="process_data",
        python_callable=process_data_fn,
        provide_context=True,
        dag=dag
    )
