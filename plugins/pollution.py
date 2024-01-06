# --------------------------------------------------------
# Grabs data from openweather.org and stores it in an InfluxDB
#
# --------------------------------------------------------
import requests
#import json
import urllib
import os


class pollution:
    vars = ["zips", "key"]

    def run(self, values):

        zips = values["zips"].split()

        for zip in zips:
            print("Getting zipcode " + zip)

            url = 'https://nominatim.openstreetmap.org/search?q=' + urllib.parse.quote(zip) + '&format=json'
            address_data = requests.get(url)
            #print(address_data.status_code)
            if(address_data.status_code != 200): raise Exception("Bad return status " + str(address_data.status_code))
            address_data = address_data.json()
            
            url = 'http://api.openweathermap.org/data/2.5/air_pollution?lat=' + \
                address_data[0]["lat"] + '&lon=' + address_data[0]["lon"] + '&appid=' + values["key"]
            json_data = requests.get(url).json()

            # print("Got this data back:")
            # print(merged_dict)

            json_body = [
                {
                    "measurement": "pollution",
                    "tags": {
                        "id": zip,
                        #"timezone":json_data["timezone"],
                        #"label": json_data["list"][0]['components']
                    },
                    "fields": json_data["list"][0]['components']
                }
            ]

            return json_body