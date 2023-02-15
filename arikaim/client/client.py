""" 
    Arikaim CMS
    http://www.arikaim.com
    Copyright (c) Konstantin Atanasov <info@arikaim.com>
    license     http://www.arikaim.com/license
"""
import http.client
import json;
import urllib.parse;
from . import apiresponse;

class ArikaimClient:
    """ Arikaim CMS api client class """

    def __init__(self, host, api_key = None, ssl = False, timeout = 10, port = 80):
        """
            Contructor

            Parameters
            ----------
            host : str
                API server host
            api_key : str
                Api key for auth
            ssl : bool
                SSL connection
            timeout : int
                Connection timeout
            port : int
                Connecrtion port
        """

        self._headers = {} 
        if ssl == False:
            self._client = http.client.HTTPConnection(host,port,timeout = timeout)
        else: 
            self._client = http.client.HTTPSConnection(host,port,timeout = timeout)
        self._endpoint = host
        self.set_api_key(api_key)
        self._headers['Content-Type'] = 'application/json'

    def set_api_key(self, api_key):
        """ Set api key """
        if api_key != '':
            self._api_key = api_key
            self._headers['Authorization'] = api_key

    def request(self, method, url, data = None, data_encode = 'json'): 
        """
            Api request main method
            Parameters
            ----------
                method : str
                    Request method
                url: str
                    Request url
                data: dictonary
                    Rquest data
                data_encode: str
                    Data encoding method 
            Returns
            -------
                ApiResponse object 
        """
        if data != None:
            if data_encode == 'json':
                data = json.dumps(data)
            else:                
                data = urllib.parse.urlencode(data)

        self._client.request(method,url,data,self._headers)
        response = self._client.getresponse()
        data = response.read()
        self._client.close()

        data = json.loads(data)

        return apiresponse.ApiResponse(data)

    def post(self, url, data = None, data_encode = 'json'):
        """ Post request """
        return self.request('POST',url,data,data_encode)

    def put(self, url, data = None, data_encode = 'json'):
        """ Put request """
        return self.request('PUT',url,data,data_encode)

    def get(self, url, data = None):
        """ Get request """
        return self.request('GET',url,data)

    def head(self, url, data = None):
        return self.request('HEAD',url,data)

    def delete(self, url, data = None):
        """ Delete """
        return self.request('DELETE',url,data)

    def patch(self, url, data = None):
        """ Patch request """
        return self.request('PATCH',url,data)
    
    def options(self, url, data = None):
        """ Options request """
        return self.request('OPTIONS',url,data)

        