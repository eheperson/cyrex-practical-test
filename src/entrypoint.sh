#!/bin/sh

if [ "$RUN" = "1" ]; then
    locust -f ./app/main.py --config ./confs/locust.docker.conf
fi

exec "$@"
