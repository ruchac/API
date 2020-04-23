import os, sys, inspect
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"subfolder")))
if cmd_subfolder not in sys.path:
     sys.path.insert(0, cmd_subfolder)
import datetime
import http.client
import json 
import hashlib
import urllib


class ActiveEnergyAPIClient(object):

    def __init__(self, protocol, host, port, api_key, secret):
        self.protocol = protocol
        self.host = host
        self.port = port
        self.api_key = api_key
        self.secret = secret
        


    def _get_timestamp(self):
        return datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')


    def _get_signature(self, json_dump, timestamp):
        to_be_signed = 'json=%s&api_key=%s&timestamp=%s&secret=%s' % (json_dump, self.api_key, timestamp, self.secret)
        to_be_signed_encoded = to_be_signed.encode()
        return hashlib.sha256(to_be_signed_encoded).hexdigest()


    def _get_connection(self):
        if self.protocol == 'http':
            return http.client.HTTPConnection(self.host, self.port)
        elif self.protocol == 'https':
            return http.client.HTTPSConnection(self.host, self.port)

    def _make_request(self, url, query):
        json_dump = json.dumps(query)
        timestamp = self._get_timestamp()
        signature = self._get_signature(json_dump, timestamp)
        print("---------------------", timestamp)
        request_data = urllib.parse.urlencode({'json': json_dump, 'api_key': self.api_key, 'timestamp': timestamp, 'signature': signature})
        connection = self._get_connection()
        connection.request('POST', url, request_data)
        response = connection.getresponse()
        assert response.status == 200
        response_data = response.read()
        connection.close()

        return json.loads(response_data)


    def query_datalogs(self, query):
        return self._make_request('/api/third-party/datalogs/query/', query)
        return self._make_request('/api/third-party/group-and-datalog/query', query)


    def query_trees(self, query):
        return self._make_request('/api/third-party/trees/query/', query)
