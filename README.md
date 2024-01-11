# Sensor Data Test - Airflow/React/Flask app

A test application hosted in a Docker Compose environment that combines an Apache Airflow implementation (that utilizes `CeleryWorker`), a Flask backend, and a React frontend. This is a proof-of-concept to demonstrate utilizing Airflow to run computations on data hosted externally (in a [data.world](https://data.world) dataset) and show a full-stack application that can query/display the resulting data, as well as interact with Airflow directly.

Data is sensor data from an instrumented electric vehicle taking various air pollutant readings. I've taken a sample of the dataset and re-uploaded to a personal data.world project for testing. The full dataset can be found here: [Identifying Air Pollution Source Impacts in Urban Communities Using Mobile Monitoring](https://data.world/us-epa-gov/124206c8-26a9-435b-9f6c-7cb0d830fbc2).

The Airflow piece was taken directly from Airflow's own documentation on running in a Docker Compose setup. I will be providing an abridged version of the documentation here, but you can refer to the official docs here for the full breakdown: [Running Airflow in Docker](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html).

## Overview

This application environment is broken into three pieces:

### Apache Airflow

Contains all the necessary components for running Airflow, including the webserver, scheduler, worker, database, and redis, among other things. 

One DAG is included, `process_sensor_data`, which does the following:

1. Creates its own Postgres db and table to store its data. In a production environment, this would be done elsewhere but for simplicity I've just included it as a step in the DAG.
2. Query a dataset from [data.world](https://data.world) using an API token, then perform some computation and store in a database table. Right now, each run produces the same data since it's computing from the entire dataset and the dataset does not change.

Note: the installation and spinning up of all the containers necessary for Airflow is pretty memory-intensive; your computer may slow down for a minute while the workload is being run.

### Flask backend

Sets up a basic API. Utilizes the Airflow API to enable a DAG and trigger a DAG run; also queries database for data. Uses basic authentication, utilizing the default credentials set up for Airflow.

### React frontend

Provides some buttons to trigger a DAG run and query db for data. Flash messages at the top to indicate status changes. Data displays in a table when available. No authentication set up, just hits the Flask API to perform tasks.
 
- create "config" file in images/airflow with the following content:
```
[DEFAULT]
auth_token = <your token here>

[r]
auth_token = <your token here>
```