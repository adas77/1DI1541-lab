#!/bin/sh
export $(grep -v '^#' .env | xargs -d '\n')
pip install -U -r src/requirements.txt
export FLASK_DEBUG=1
flask run --debugger --host=$FLASK_HOST --port=$FLASK_PORT
