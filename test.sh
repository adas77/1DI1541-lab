#!/bin/sh
export $(grep -v '^#' .env | xargs -d '\n')
cd src
pytest -rP db_test.py 
