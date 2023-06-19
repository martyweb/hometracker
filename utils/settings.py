# import json

class settings:
    '''
    Application Settings
    '''

    def get_values():
        with open('config-app.json', 'r') as f:
            data = json.load(f)

        return data