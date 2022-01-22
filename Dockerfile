FROM ubuntu:18.04
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
#RUN apt-get install mysql-server
#FROM python:3
ENV influxdbhost="192.168.103.111"
ENV influxdbport="8086"
ENV influxdbusername="test"
ENV influxdbpass="test"
ENV influxdbdatabase="HomeStatus"

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]