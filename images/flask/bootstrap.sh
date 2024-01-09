#!/bin/bash

# app prereqs
until cd /root/app && pip install -r requirements.txt
do
    echo "Waiting to install app dependencies..."
done

pip install -r requirements-test.txt

python3 -m flask run --host=0.0.0.0 --port=8000 --debug