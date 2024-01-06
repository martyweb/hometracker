from influxdb_client import InfluxDBClient, Point, WritePrecision, domain
from influxdb_client.client.exceptions import InfluxDBError
from influxdb_client.client.write_api import SYNCHRONOUS
import os
import json


class extInflux2:
    _client = False
    _lastError = ""
    _host = ""
    _org = ""
    _token = ""
    _bucket = ""

    def __init__(self, host, token, org, bucket):
        self._host = host
        self._token = token
        self._org = org
        self._bucket = bucket
        self.checkConnectivity()
        # self.data = []

    def config(self):
        return {"host": self._host}

    def checkConnectivity(self):
        ready = False
        try:
            self._client = InfluxDBClient(
                url=self._host, token=self._token, org=self._org)

            if self._bucket is not None:
                influxdb_buckets_api = self._client.buckets_api()
                my_bucket = influxdb_buckets_api.find_bucket_by_name(
                    self._bucket)
                if my_bucket is None:
                    self.createbucket(self._bucket)

            ready = self._client.ready()

        except Exception as e:
            print(e)
            #self._lastError = e.content
            return False

        return ready

    def createbucket(self, bucketname):

        influxdb_orgs_api = self._client.organizations_api()
        org_info = influxdb_orgs_api.find_organizations(org=self._org)

        influxdb_buckets_api = self._client.buckets_api()
        new_bucket = domain.bucket.Bucket(
            name=bucketname,
            retention_rules=[],
            description="Data for HomeStatus application",
            org_id=org_info[0].id
        )
        influxdb_buckets_api.create_bucket(new_bucket)
        return True

        # except InfluxDBClientError as e:
        # return e.content

    def sendToInflux(self, json_data, bucket=None):

        if bucket is None and self._bucket is not None:
            bucket = self._bucket

        point = Point.from_dict(
            json_data,
            WritePrecision.MS
        )

        try:
            influxdb_write_api = self._client.write_api(
                write_options=SYNCHRONOUS)
            # print("writing")
            # print(bucket)
            # print(self._org)
            # print(json)
            response = influxdb_write_api.write(
                bucket=bucket, org=self._org, record=point)

            #print("InfluxDB client response: ", response)
            #print("JSON sent: ", json_body)
            return response

        except Exception as e:
            print(e)
            #self._lastError = e.content
            return e

    def success_cb(self, details, data):
        url, token, org = details
        print(url, token, org)
        data = data.decode('utf-8').split('\n')
        print('Total Rows Inserted:', len(data))

    def error_cb(self, details, data, exception):
        print(exception)

    def retry_cb(self, details, data, exception):
        print('Retrying because of an exception:', exception)
