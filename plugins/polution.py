#--------------------------------------------------------
#Grabs data from openweather.org and stores it in an InfluxDB
#
#--------------------------------------------------------
import requests
import json
import urllib


class polution:
    vars = ["zips","key"]

    def run(self, values):

        zips = values["zips"].split()

        for zip in zips:
            print("Getting zipcode " + zip)

            url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(zip) +'?format=json'
            adress_data = requests.get(url).json()

            url = 'http://api.openweathermap.org/data/2.5/air_pollution?lat=' + adress_data[0]["lat"] + '&lon=' + adress_data[0]["lon"] + '&appid=' +  values["key"]
            json_data = requests.get(url).json()

            # print("Got this data back:")
            # print(merged_dict)

            json_body = [
            {
                "measurement": "main",
                "tags": {
                    "id": zip,
                    #"timezone":json_data["timezone"],
                    #"label": json_data["list"][0]['components']
                },
                "fields": json_data["list"][0]['components']
            }
            ]

            return json_body

