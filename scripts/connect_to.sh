#!/bin/bash

# connect_to.sh <SERVICE>

docker-compose -f docker-compose.yml exec $1 /bin/bash