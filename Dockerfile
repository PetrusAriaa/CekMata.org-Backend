FROM python:3.10.13-alpine3.19
WORKDIR /app

COPY requirements.txt .

RUN \
    pip install --upgrade pip && \
    pip install -r requirements.txt --no-cache-dir

COPY . .