#!/bin/sh
pip install -U -r src/requirements.txt
export $(grep -v '^#' .env | xargs -d '\n')
export FLASK_DEBUG=1
flask run --debugger --host=$FLASK_HOST --port=$FLASK_PORT
