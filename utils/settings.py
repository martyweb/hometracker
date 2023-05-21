# import json

class settings:
    '''
    Application Settings
    '''

    def get_values():

        return {
            "influxdbhost": "192.168.103.122",
            "influxdbport": "8086",
            "influxdbusername": "test",
            "influxdbpass": "test",
            "influxdbdatabase":"HomeStatus",
            "db_file": "database.db",
            "plugin_path": "plugins",
            "db_path": "db",
            "granfana_host": "https://grafana.martyweb.com",
        }