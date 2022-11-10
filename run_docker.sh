#!/bin/sh
export $(grep -v '^#' .env | xargs -d '\n')
[ -n "$(docker images -q $DOCKER_IMAGE_NAME)" ] || docker build --tag $DOCKER_IMAGE_NAME .
# docker build --tag $DOCKER_IMAGE_NAME
echo "RUNNING ON PORT: $FLASK_DOCKER_PORT"
docker run -v $DOCKER_DB_PATH:/src/instance --publish $FLASK_DOCKER_PORT:5000 $DOCKER_IMAGE_NAME
