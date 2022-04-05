from influxdb import InfluxDBClient
from influxdb.client import InfluxDBClientError
import os


class extInflux:
    _client = False
    _lastError = ""
    _host = ""
    _port = ""
    _username = ""
    _password = ""
    _database = ""

    def __init__(self, host, port, username, password, database):
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self._database = database
        self.checkConnectivity()
        # self.data = []

    def config(self):
        return {"host": self._host, "port": self._port}

    def checkConnectivity(self):
        try:
            self._client = InfluxDBClient(
                self._host, self._port, self._username, self._password, self._database
            )

            if self._database in self._client.get_list_database():
                return True
            else:
                self.createdb(self._database)
                return False

        except InfluxDBClientError as e:
            self._lastError = e.content
            return False

            # return False

    def createdb(self, dbname):
        # try:
        self._client.create_database(dbname)
        return True

        # except InfluxDBClientError as e:
        # return e.content

    def sendToInflux(json_body):

        client = InfluxDBClient(
            host=os.environ["influxdbhost"],
            port=os.environ["influxdbport"],
            username=os.environ["influxdbusername"],
            password=os.environ["influxdbpass"],
            database=os.environ["influxdbdatabase"],
        )

        try:
            response = client.write_points(json_body)
            # print("InfluxDB client response: ", response)
            # print("JSON sent: ", json_body)
            return response

        except InfluxDBClientError as e:
            return e.content
