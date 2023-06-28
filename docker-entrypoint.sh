#!/bin/bash -x

# Wait for few seconds and run db migrations
if [[ "${1}" == "create" ]]; then
    exec gunicorn --bind 0.0.0.0:8000 imagify_backend.wsgi
elif [[ "${1}" == "rq-worker-default" ]]; then
    exec python3 manage.py rqworker default
fi
