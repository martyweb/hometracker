import requests
import json


class weather:

        #def __init__(self):
        #        return 0

        #--------------------------------------------------------
        #Get weather information from openweather
        #--------------------------------------------------------
        def run(self, zip, appid):
                        
                url = "https://api.openweathermap.org/data/2.5/weather?zip="+zip+"&APPID="+appid+"&units=imperial"
                response = requests.request("GET", url)
                json_data = json.loads(response.text)

                json_data["main"]['temp_max'] = int(json_data["main"]['temp_max'])
                json_data["main"]['temp_min'] = int(json_data["main"]['temp_min'])

                json_body = [
                        {
                        "measurement": "main",
                        "tags": {
                                "zip": zip,
                                "timezone":json_data["timezone"],
                                "name":json_data["name"]
                                },
                        "fields": json_data["main"]
                        }
                        ]

                return json_body

