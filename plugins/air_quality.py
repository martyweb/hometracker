import requests
import json


class air_quality:
    _ids = []
    vars = ["ids"]

    def run(self, values):

        id_arry = values["ids"].split()

        for id in id_arry:
            print("Getting id " + id)

            url = "https://api.purpleair.com/v1/sensors/"+id
            headers = {'X-API-Key': values["key"]}
            response = requests.request("GET", url, headers=headers)
            json_data = json.loads(response.text)

            #print("Got this data back:")
            #print(json_data)

            #remove all stats nodes b/c it was causing problems
            temp_data=[]
            for data in json_data["sensor"]:
                if "stats" in data:
                    temp_data.append(data)
            for remove in temp_data:
                del json_data["sensor"][remove]

            #post data to influxdb
            json_body = [
                {
                    "measurement": "air_quality",
                    "tags": {
                        "id": id,
                        #"timezone":json_data["timezone"],
                        "label":json_data["sensor"]["name"]
                    },
                    "fields": json_data["sensor"]
                }
            ]

            return json_body
