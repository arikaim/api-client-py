""" 
    Arikaim CMS
    http://www.arikaim.com
    Copyright (c) Konstantin Atanasov <info@arikaim.com>
    license     http://www.arikaim.com/license
"""
import json

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
            data = json.loads(data)
        
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
        