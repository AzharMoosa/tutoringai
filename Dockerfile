FROM node:latest as build
WORKDIR /frontend
COPY ./frontend/package.json ./
COPY ./frontend/package-lock.json ./
RUN npm ci
COPY ./frontend ./
RUN npm run build

FROM python:3.9.7

WORKDIR /

COPY . .

ENV DISPLAY=:99

RUN apt-get -y update
RUN apt-get install -y python3 python3-pip
RUN pip3 install -r requirements.txt

COPY --from=build /frontend/build/ ./frontend/build/

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "1", "--worker-class", "eventlet", "app:app"]
