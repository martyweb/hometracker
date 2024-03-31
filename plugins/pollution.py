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

            url = 'http://api.openweathermap.org/geo/1.0/zip?zip=' + \
                urllib.parse.quote(zip) + ',' + \
                'US' + '&appid=' + values["key"]
                        
            address_data = requests.get(url)
            #print(address_data.json())
            if(address_data.status_code != 200):
                raise Exception("Bad return status " +
                                str(address_data.status_code))
            address_data = address_data.json()

            print("Getting pollution for " + str(address_data["lat"]) + " " + str(address_data["lon"]))

            url = 'http://api.openweathermap.org/data/2.5/air_pollution?lat=' + \
                str(address_data["lat"]) + '&lon=' + \
                str(address_data["lon"]) + '&appid=' + values["key"]
            json_data = requests.get(url).json()

            # print("Got this data back:")
            # print(merged_dict)

            json_body = [
                {
                    "measurement": "pollution",
                    "tags": {
                        "id": zip,
                        # "timezone":json_data["timezone"],
                        # "label": json_data["list"][0]['components']
                    },
                    "fields": json_data["list"][0]['components']
                }
            ]

            return json_body
