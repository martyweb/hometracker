import json
import os


class plugins:
    '''
    Plugin utils
    '''
    def get_values():

        with open('config-plugins.json', 'r') as f:
            data = json.load(f)

        # TODO: check data from file that it conforms to standards

        return data

        # return {
        #     "air_quality": {"ids": "22553", "key": "7B5CF0D1-ECD4-11EC-8561-42010A800005", "interval": 60},
        #     "weather": {"appid": "15c6d1063b5b819c4a1eb6e47dc8dd4b", "zip": "60564", "interval": 60},
        #     "speed_test": {"zip": "60564", "interval": 60},
        #     "pollution": {"zips": "60564", "key": "15c6d1063b5b819c4a1eb6e47dc8dd4b", "interval": 60},
        # }

    def get_plugins():
        plugin_names = []
        for file in os.listdir(os.environ["plugin_path"]):
            if "__" not in file and ".py" in file:
                plugin_name = file.replace(".py", "")
                plugin_names.append(plugin_name)

        return plugin_names
