FROM python:3.10-slim-buster
WORKDIR /app
COPY . .

RUN apt update -y

RUN apt-get update && pip install -r reqirement.txt
CMD [ "python3", "app.py" ]