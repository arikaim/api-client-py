""" 
    Arikaim CMS
    http://www.arikaim.com
    Copyright (c) Konstantin Atanasov <info@arikaim.com>
    license     http://www.arikaim.com/license
"""
import requests
from base64 import b64decode
from json import dumps, JSONDecodeError
import urllib.parse;
from .apiresponse import ApiResponse;


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

    def add_haader(self, item: any):
        self._headers.update(item)

    def set_api_key(self, api_key: str):
        """ Set api key """
        self._api_key = api_key.strip()

        if api_key != '':           
            self._headers['Authorization'] = self._api_key

    def request(self, method: str, path: str, data: any = None, data_encode: str = 'json') -> ApiResponse:
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
                data = dumps(data)
            else:                
                data = urllib.parse.urlencode(data)

        url = self._endpoint + path

        response = requests.request(
            method = method,
            url = url, 
            data = data, 
            headers = self._headers
        )

        try:
            data = response.json()
        except JSONDecodeError:
            data = {
                'result': None,
                'status': 'error',
                'errors': 'Server response error',
                'code'  : 500
            }

        response.close()
        return ApiResponse(data)

    def uploadFile(self, path: str, file_name: str, data: any = None, method: str = 'POST') -> ApiResponse:
        self._headers.pop('Content-Type')
        if not data:
            data = {}
        
        data['file'] = open(file_name,'rb')

        response = requests.request(
            method = method,
            url = self._endpoint + path,            
            files = data,
            headers = self._headers
        )

        data = response.json()
        response.close()
     
        return ApiResponse(data)
    
    def post(self, path: str, data: any = None, data_encode: str = 'json') ->ApiResponse:
        """ Post request """
        return self.request('POST',path,data,data_encode)

    def put(self, path: str, data: any = None, data_encode: str = 'json') -> ApiResponse:
        """ Put request """
        return self.request('PUT',path,data,data_encode)

    def get(self, path: str, data: any = None) -> ApiResponse:
        """ Get request """
        return self.request('GET',path,data)

    def head(self, path: str, data: any = None) -> ApiResponse:
        return self.request('HEAD',path,data)

    def delete(self, path: str, data: any = None) -> ApiResponse:
        """ Delete """
        return self.request('DELETE',path,data)

    def patch(self, path: str, data: any = None) -> ApiResponse:
        """ Patch request """
        return self.request('PATCH',path,data)
    
    def options(self, path: str, data: any = None) -> ApiResponse:
        """ Options request """
        return self.request('OPTIONS',path,data)

    def save_ecoded_file(self, response: ApiResponse, field_name: str, file_name: str) -> bool:
        data = response.get(field_name)
        if not data:
            return False

        if is_encoded(data) == True:
            data = b64decode(data)

        try:
            file = open(file_name,'wb')
            file.write(data)
            file.close()
            return True
        except Exception as error:
            print(error)
            return False

       
def is_encoded(data):
    try:
        b64decode(data,validate = True)
        return True
    except:
        return False