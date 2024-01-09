#!/bin/bash

# app prereqs
until cd /root/app
do
    echo "Waiting to install app dependencies..."
done
npm install

HOST=0.0.0.0 PORT=3000 npm start