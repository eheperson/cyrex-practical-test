#!/bin/sh

if [ "$RUN" = "1" ]; then
    locust -f ./main.py --config ./locust.conf
fi

exec "$@"
