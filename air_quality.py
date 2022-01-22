import requests
import json

class air_quality:

    def run(self, ids):
        id_arry=ids.split()

        for id in id_arry:
            print("Getting id " + id)

            url = "https://www.purpleair.com/json?show="+id
            response = requests.request("GET", url)
            json_data = json.loads(response.text)

            #print("Got this data back:")
            stats=json.loads(json_data["results"][0]["Stats"])
            del json_data["results"][0]["Stats"]
            metadata=json_data["results"][0]
            merged_dict = {**metadata, **stats}
            #print(merged_dict)

            json_body = [
                {
                    "measurement": "main",
                    "tags": {
                        "id": id,
                        #"timezone":json_data["timezone"],
                        "label":merged_dict["Label"]
                    },
                    "fields": merged_dict
                }
            ]

            return json_body
