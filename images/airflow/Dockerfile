FROM apache/airflow:2.8.0
ADD requirements.txt .
RUN pip install apache-airflow==2.8.0 -r requirements.txt
RUN dw -p r configure -t ${DATA_DOT_WORLD_TOKEN}