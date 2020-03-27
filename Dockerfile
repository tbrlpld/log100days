FROM python:3.8.2-alpine

WORKDIR /usr/src/app

RUN apk add build-base

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT hypercorn --workers 3 --bind 0:5000 log100days:app
EXPOSE 5000 