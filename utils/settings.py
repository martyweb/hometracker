import json
import os

class settings:
    '''
    Application Settings
    '''
    def get_values():
        with open('config-app.json', 'r') as f:
            data = json.load(f)

        #override with env vars
        for setting in data:
            if os.getenv(setting) is not None: data[setting]=os.getenv(setting)

        #TODO: check data from file

        return data