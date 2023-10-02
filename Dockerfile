FROM python:3.11

WORKDIR /app

RUN mkdir datasets

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .