import os

from airflow.operators.python_operator import PythonOperator

import psycopg2
from psycopg2 import sql


def setup_db_fn():
    """
    Create database and table in Postgres
    """
    pg_user = os.getenv('POSTGRES_USER')
    pg_pw = os.getenv('POSTGRES_PASSWORD')
    db = os.getenv('SENSOR_DATA_DB')
    conn = psycopg2.connect(
        user=pg_user,
        password=pg_pw,
        host="postgres",
        dbname="airflow"
    )
    conn.autocommit = True
    cur = conn.cursor()
    # create db
    try:
        cur.execute(sql.SQL('CREATE DATABASE {};').format(
            sql.Identifier(db)))
    except (psycopg2.errors.DuplicateDatabase, psycopg2.errors.UniqueViolation):
        pass
    conn.close()
    # create table
    conn = psycopg2.connect(
        user=pg_user,
        password=pg_pw,
        host="postgres",
        dbname=db
    )
    conn.autocommit = True
    cur = conn.cursor()
    query = """CREATE TABLE IF NOT EXISTS sensor_data (
        id int primary key generated always as identity, 
        run_id varchar,
        ufp_mean decimal,
        ufp_median decimal,
        ufp_stddev decimal,
        bc_mean decimal,
        bc_median decimal,
        bc_stddev decimal,
        no2_mean decimal,
        no2_median decimal,
        no2_stddev decimal,
        created_at timestamp
    )"""
    cur.execute(query)
    conn.close()


def setup_db(dag):
    return PythonOperator(
        task_id="setup_db",
        python_callable=setup_db_fn,
        dag=dag
    )
