#!/bin/sh
export $(grep -v '^#' .env | xargs -d '\n')
[ -n "$(docker images -q $DOCKER_IMAGE_NAME)" ] || sudo docker build --tag $DOCKER_IMAGE_NAME .
sudo docker build --tag $DOCKER_IMAGE_NAME .
echo "RUNNING ON PORT: $FLASK_DOCKER_PORT"
sudo docker run --publish $FLASK_DOCKER_PORT:5000 $DOCKER_IMAGE_NAME
