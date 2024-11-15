""" 
    Arikaim CMS
    http://www.arikaim.com
    Copyright (c) Konstantin Atanasov <info@arikaim.com>
    license     http://www.arikaim.com/license
"""
import requests
from base64 import b64decode
from json import dumps, JSONDecodeError, loads
import urllib.parse;
import os


class ApiResponse:
    """ Api response class """

    def __init__(self, data = None):   
        self.clear()
        self.parse(data)

    def clear(self):
        self._status = 'ok'
        self._errors = []
        self._code = 200 
        self._result = {}

    def parse(self,data: any):
        if type(data) == str:
            data = loads(data)
        
        if (type(data) is dict):
            self._status = data['status']
            self._errors = data['errors']
            self._code = data['code']
            self._result = data['result']
            return True
        return False

    def to_dictonary(self):       
        return {
            'result': self._result,
            'status': self._status,
            'errors': self._errors,
            'code'  : self._code
        }
     
    def has_error(self):
        return len(self._errors) > 0

    @property
    def errors(self):
        return self._errors

    @property
    def result(self, value: any):
        self._result = value

    @property
    def result(self):
        return self._result

    @property
    def status(self, value: any):
        self._status = value
    
    @property
    def status(self):
        return self._status

    @property
    def code(self, value: any):
        self._code = value

    @property
    def code(self):
        return self._code

    def get(self, key: str):
        return self._result[key]

    def field(self, key: str, value: any):
        self._result[key] = value

    def add_error(self, error: str):
        self._errors.append(error)
      
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

    def remove_haader(self, key: any):
        self._headers.pop(key)

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


    def upload(self, 
        path: str, 
        file_name: str, 
        field_name: str = 'file', 
        data: dict = {}, 
        method: str = 'POST'
    ) -> ApiResponse: 
        headers = self._headers
        headers.pop('Content-Type')

        if os.path.isfile(file_name) == False:          
            raise Exception('File not exist')
        
        files = {
            field_name: open(file_name,'rb')
        }
     
        response = requests.request(
            method = method,
            url = self._endpoint + path,            
            files = files,
            data = data,
            headers = headers
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