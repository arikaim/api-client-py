""" 
    Arikaim CMS
    http://www.arikaim.com
    Copyright (c) Konstantin Atanasov <info@arikaim.com>
    license     http://www.arikaim.com/license
"""
import requests

import json;
import urllib.parse;
from . import apiresponse;

class ArikaimClient:
    """ Arikaim CMS api client class """

    def __init__(self, host, api_key = None):
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
        self._endpoint = host
        self.set_api_key(api_key)
        self._headers['Content-Type'] = 'application/json'

    def add_haader(self, item):
        self._headers.update(item)

    def set_api_key(self, api_key: str):
        """ Set api key """
        self._api_key = api_key.strip()

        if api_key != '':           
            self._headers['Authorization'] = self._api_key

    def request(self, method, path, data = None, data_encode = 'json'): 
        """
            Api request main method
            Parameters
            ----------
                method : str
                    Request method
                path: str
                    Request path
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

        url = self._endpoint + path

        response = requests.request(method = method,url = url, data = data, headers = self._headers)
        data = response.json()
        response.close()
     
        return apiresponse.ApiResponse(data)

    def post(self, path, data = None, data_encode = 'json'):
        """ Post request """
        return self.request('POST',path,data,data_encode)

    def put(self, path, data = None, data_encode = 'json'):
        """ Put request """
        return self.request('PUT',path,data,data_encode)

    def get(self, path, data = None):
        """ Get request """
        return self.request('GET',path,data)

    def head(self, path, data = None):
        return self.request('HEAD',path,data)

    def delete(self, path, data = None):
        """ Delete """
        return self.request('DELETE',path,data)

    def patch(self, path, data = None):
        """ Patch request """
        return self.request('PATCH',path,data)
    
    def options(self, path, data = None):
        """ Options request """
        return self.request('OPTIONS',path,data)

        