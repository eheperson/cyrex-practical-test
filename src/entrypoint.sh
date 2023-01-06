#!/bin/sh

if [ "$RUN" = "1" ]; then
    locust -f ./main.py --config ./locust.docker.conf
fi

exec "$@"
