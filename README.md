# Sensor Data Test - Airflow/React/Flask app

A test application hosted in a Docker Compose environment that combines an Apache Airflow implementation (that utilizes `CeleryWorker`), a Flask backend, and a React frontend. This is a proof-of-concept to demonstrate utilizing Airflow to run computations on data hosted externally (in a [data.world](https://data.world) dataset) and show a full-stack application that can query/display the resulting data, as well as interact with Airflow directly.

Data is sensor data from an instrumented electric vehicle taking various air pollutant readings. I've taken a sample of the dataset and re-uploaded to a personal data.world project for testing. The full dataset can be found here: [Identifying Air Pollution Source Impacts in Urban Communities Using Mobile Monitoring](https://data.world/us-epa-gov/124206c8-26a9-435b-9f6c-7cb0d830fbc2).

The Airflow piece was taken directly from Airflow's own documentation on running in a Docker Compose setup. I will be providing an abridged version of the documentation here, but you can refer to the official docs here for the full breakdown: [Running Airflow in Docker](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html).

The code and files for all the application parts reside in the `apps` folder, each with their own folder. The Dockerfiles and relevant files for all the application parts reside in the `images` folder, similarly each with their own folder.

Environment variables are utilized throughout for credentials.

## Overview

This application environment is broken into three pieces:

### Apache Airflow

Contains all the necessary components for running Airflow. Here are the service definitions:

- `airflow-scheduler` - The scheduler monitors all tasks and DAGs, then triggers the task instances once their dependencies are complete.
- `airflow-webserver` - The webserver is available at http://localhost:8080.
- `airflow-worker` - The worker that executes the tasks given by the scheduler.
- `airflow-triggerer` - The triggerer runs an event loop for deferrable tasks.
- `airflow-init` - The initialization service.
- `postgres` - The database.
- `redis` - The redis broker that forwards messages from scheduler to worker.

Optionally, you can enable `flower` by adding `--profile flower` option, e.g. `docker compose --profile flower up`, or by explicitly specifying it on the command line e.g. `docker compose up flower`.

- `flower` - The flower app for monitoring the environment. It is available at http://localhost:5555.

All these services allow you to run Airflow with [CeleryExecutor](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/executor/celery.html). For more information, see [Architecture Overview](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/overview.html).

DAG definitions can be found in `apps/airflow/dags`. One DAG is included, `process_sensor_data`, which does the following:

1. Creates its own Postgres db and table to store its data. In a production environment, this would be done elsewhere but for simplicity I've just included it as a step in the DAG.
2. Query a dataset from [data.world](https://data.world) using an API token, then perform some computation and store in a database table. Right now, each run produces the same data since it's computing from the entire dataset and the dataset does not change.

Note: the installation and spinning up of all the containers necessary for Airflow is pretty memory-intensive; your computer may slow down for a minute while the workload is being run.

### Flask backend

Available at http://localhost:8000.

Sets up a basic API. Utilizes the Airflow API to enable a DAG and trigger a DAG run; also queries database for data. Uses basic authentication, utilizing the default credentials set up for Airflow.

### React frontend

Available at http://localhost:3000.

Set up using [create-react-app](https://github.com/facebook/create-react-app) and comes with hot reloading. View those docs for more info.

Provides some buttons to trigger a DAG run and query db for data. Flash messages at the top to indicate status changes. Data displays in a table when available. No authentication set up, just hits the Flask API to perform tasks.

## Setup

Make sure you have Docker or Docker Desktop installed on your machine, and at least 4 GB of memory is allocated to Docker. Additionally, make sure you have Docker Compose v2.14.0 or newer installed on your machine.

You can check if you have enough memory by running this command:

```bash
docker run --rm "debian:bullseye-slim" bash -c 'numfmt --to iec $(echo $(($(getconf _PHYS_PAGES) * $(getconf PAGE_SIZE))))'
```

**Set up data.world**

You'll need to create a [data.world](https://data.world) account. Once you have an account, you'll need to enable the Python integration. Then, go to your profile, then Advanced, then copy the API token for the Read/Write scope. Keep this in a safe place.

**Create necessary files**

1. Create the `logs` and `plugins` folder for Airflow, under `apps/airflow`. These are necessary for Airflow.
2. Create a `.env` file in the project base directory with the string "AIRFLOW_UID=5000".
3. Create a file called `config` within `images/airflow` with the following content:
```
[DEFAULT]
auth_token = <your token here>

[r]
auth_token = <your token here>
```
Replace `<your token here>` with the data.world API token you retrieved above.

Normally, you would configure the `datadotworld` Python library by calling `dw configure -t <token>` but I couldn't get that to work in the container setup, so I resorted to creating the file manually and copying it into place instead. It's hacky but it works.

Note: supposedly, only the "default" config is necessary, but during my testing, I ended up needing an "r" section as well, for reading files.

**Initialize Airflow**

Next, on **all operating systems**, you need to run database migrations and create the first user account. To do this, run.

```bash
docker compose up airflow-init
```

After initialization is complete, you should see a message like this:

```
airflow-init_1        | Upgrades done
airflow-init_1        | Admin user airflow created
airflow-init_1        | 
start_airflow-init_1 exited with code 0
```

The account created has the login `airflow` and the password `airflow`.

**Initialize all services**

Now we can run Airflow and initialize the rest of the services.

```bash
docker compose up
```

Add `-d` to run in detached mode.

You can view the status of all containers by pulling up Docker Desktop or by running `docker ps`.

## Usage

**Accessing the Airflow web interface**

Once the cluster has started up, you can log in to the web interface and begin experimenting with DAGs.

The webserver is available at: `http://localhost:8080`. The default account has the login `airflow` and the password `airflow`.

Note: The Airflow webserver may not be available immediately after all services have returned a `Started` state. I've found it is usually available after waiting a minute or two from this point.

**Sending requests to the Airflow REST API**

Basic username password authentication is currently supported for the REST API, which means you can use common tools to send requests to the API.

The webserver is available at: `http://localhost:8080`. The default account has the login `airflow` and the password `airflow`.

**View logs**

There are three ways to view the logs of a particular service:

You can use the handy `show_logs` script.
```bash
scripts/show_logs.sh SERVICE
```
Where SERVICE is the name of the service in the `docker-compose.yml` file.

You can also run the command directly:
```bash
docker logs -t -f sensor-data-airflow-react-flask-SERVICE-1
```
The suffix `-1` just means we're running a single container of that service.

Finally, you can also go to Docker Desktop, click Containers, click the arrow next to our Compose environment to expand the containers list, then just click the name of the container. You'll be taken to the Logs tab.

**Connect to a service directly**

There are three ways to connect to a particular service's container directly:

You can use the handy `connect_to` script to connect to a service's container directly.
```bash
scripts/connect_to.sh SERVICE
```
Where SERVICE is the name of the service in the `docker-compose.yml` file.

You can also run the command directly.
```bash
docker compose -f docker-compose.yml exec SERVICE /bin/bash
```
The suffix `-1` just means we're running a single container of that service.

Finally, you can also go to Docker Desktop, click Containers, click the arrow next to our Compose environment to expand the containers list, then click the three dots for the container you wish to connect to and select Open in Terminal. Alternatively, click the name of the container, then select the Terminal tab.

**Stop/shutdown the environment**

Stopping the environment will "pause" the containers but not destroy them. If we shutdown the environment, we will destroy the containers and the internal network. Our volumes and images will remain, however, unless we specify to destroy them too.

If you are running the environment in attached mode, hitting Ctrl+C *stops* the environment, it does not shut it down.
```
# to stop...
docker compose stop

# to shutdown...
docker compose down

# to shutdown and delete volumes, containers, and images...
docker compose down --volumes --remove-orphans --rmi all
```
The final option is recommended for this particular app environment.

To start it back up, we'll need to do `docker compose up airflow-init` again first, then use `docker compose up` (remember `-d` if using detached mode).

## Perform a full end-to-end test

Open Airflow in your browser. Ensure the webserver is active and log in using the credentials listed above. Ensure there are one or more DAGs available to run. Now visit the React frontend at `http://localhost:3000`. Click "Trigger DAG" and confirm the progress over in Airflow. Once the DAG has completed running, go back to the React app and click "Refresh Data". You should now see a table of data.