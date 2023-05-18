FROM python:3.11-slim

RUN pip install --upgrade pip

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
