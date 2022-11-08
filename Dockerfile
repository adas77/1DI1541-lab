FROM python:3.8-slim-buster

VOLUME /src/instance
WORKDIR /src

COPY src/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0"]
# CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0", "--port=FLASK_DOCKER_PORT"]
