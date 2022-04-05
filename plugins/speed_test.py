import requests
import json
import os


# --------------------------------------------------------
# Grabs data from speedtest-cli app
# --------------------------------------------------------
class speed_test:

    vars = []

    def run(self, values):

        # linux command
        script_response = os.popen("speedtest-cli --json").read()
        # windows command
        # script_response = os.popen("C:\\Users\\marty\\AppData\\Local\\Packages\\PythonSoftwareFoundation.Python.3.8_qbz5n2kfra8p0\\LocalCache\\local-packages\\Python38\\Scripts\\speedtest-cli --json").read()

        # convert string to json object
        json_full_data = json.loads(script_response)
        json_speed_data = json_full_data
        name = json_full_data["client"]["ip"]
        json_speed_data.pop("client", None)
        json_speed_data.pop("server", None)

        # --------------------------------------------------------
        # post data to influxdb
        # --------------------------------------------------------
        json_body = [
            {
                "measurement": "speedtestdata",
                "tags": {"name": name},
                "fields": json_speed_data,
            }
        ]

        return json_body
