#!/bin/bash

source ./docker/.env
echo "wait for ${PROJECT_NAME}-db-1"

MAX_ATTEMPTS=60
for ((i=1; i <= $MAX_ATTEMPTS; i++)); do
    HELTHCHECK_STATE=$(docker inspect --format='{{json .State.Health}}' ${PROJECT_NAME}-db-1 | grep healthy)

    # echo "healthcheck_state: ${HELTHCHECK_STATE}"
    if [ "$HELTHCHECK_STATE" != "" ]; then
        echo "db is healthy"
        break
    fi

    sleep 1;
done;
