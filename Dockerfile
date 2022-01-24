#FROM ubuntu:18.04
FROM python:3.8.10

RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential

EXPOSE 5000

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
#CMD ["python", "app.py"]
CMD ["flask", "run", "--host", "0.0.0.0"]