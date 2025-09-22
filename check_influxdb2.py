# import pytest
# import app
import os
from utils.influx2_utils import extInflux2

host=os.environ["influxdbhost"],
port=os.environ["influxdbport"],
username=os.environ["influxdbusername"],
password=os.environ["influxdbpass"],
database=os.environ["influxdbdatabase"],

infdb2 = extInflux2(host,"", "HomeStatus", "HomeStatus")
response = infdb2.checkConnectivity()
print(response)

buckets_api = infdb2._client.buckets_api()
buckets = buckets_api.find_buckets()
my_bucket = buckets_api.find_bucket_by_name('my_bucket')
print(buckets)

json = [{'measurement': 'weather', 'tags': {'zip': 60564, 'timezone': -18000, 'name': 'Naperville'},
         'fields': {'temp': 70.39, 'feels_like': 71.51, 'temp_min': 68, 'temp_max': 72, 'pressure': 1013, 'humidity': 93}}]
response = infdb2.sendToInflux(json[0])
print(response)
