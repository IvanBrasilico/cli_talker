'''Classes that do the binding between "Commands" and Object/Data
Access like REST APIs, DataBase, ORM, etc.
Allow implementing a "command line  interface" for this type of access
'''
import json

import cli_talker.localizations
import requests


class Maitre():
    '''Waiter Factory/Manager'''

    def __init__(self):
        self.waiter_dict = {}

    def process_order(self, porder):
        '''porder is a Dict on format:
        'type': Type of Waiter implementation(Example: 'sqlalchemy', 'json_api')
                (required)
        Returns a waiter of correct type
        '''
        waiter_type = porder.get('type')
        if waiter_type is None:
            raise AttributeError(
                _('Misconfiguration Error. Parameter "type" needed'))
        # Discover the rigth CLASS
        waiter_class = self.waiter_dict[waiter_type]
        # Instatiate a OBJECT of the Class
        assigned_waiter = waiter_class()
        return assigned_waiter

    def add_waiter(self, waiter_dict):
        '''Receives a dict of available waiters, by type.
        'waiter_type': waiter_class
        '''
        if self.waiter_dict == {}:
            self.waiter_dict = waiter_dict
        else:
            self.waiter_dict.update(waiter_dict)


class BaseWaiter():
    '''Base Waiter with abstract methods just for test.
    A Waiter must implement the action methods
    '''

    def __init__(self):
        self.method_binder = {'GET': self.get_method,
                              'POST': self.post_method,
                              'PUT': self.put_method,
                              'DELETE': self.delete_method}
        self.response = None
        self.error = None

    def process_order(self, porder):
        '''Calls the right method to handle the order
        porder is a Dict on format:
        'method': ['GET', 'POST', 'PUT', 'DELETE'] (required)
        'params': dict or list of params fieldname:value (optional)
        '''
        order_method = porder.get('method')
        if order_method is None:
            raise AttributeError(
                _('Misconfiguration Error. Parameter "method" needed'))
        method = self.method_binder[order_method]
        resource = porder.get('resource')
        if resource is None:
            raise AttributeError(
                _('Misconfiguration Error. Parameter "resource" needed'))
        params = porder.get('params')

        return method(resource, params)

    def get_method(self, resource, params):
        return self.get_method

    def post_method(self, resource, params):
        return self.post_method

    def put_method(self, resource, params):
        return self.put_method

    def delete_method(self, resource, params):
        return self.delete_method


class RESTWaiter(BaseWaiter):
    '''Implements methods to handle a REST API communication/binding
    All methods receive resource (a URL) and parameters and
    return response, error and status_code'''

    def get_method(self, resource, params=None):
        _data = {}
        if params is None:
            pass
        elif isinstance(params, list):
            resource = resource + '%20'.join(params)
        elif isinstance(params, str):
            resource = resource + '/%s' % params
        elif isinstance(params, dict):
            _data = params
            _pk = params.pop('pk', None)
            if _pk is not None:
                resource = resource + '/%s' % _pk

        response = requests.get(resource, data=_data,
                                headers={'content-type': 'application/json'})
        if response.status_code == 200:  # Success
            return response.text, None, response.status_code
        # Failure
        return None, response.text, response.status_code

    def post_method(self, resource, params):
        if (params is None) or (params == {}):
            raise AttributeError(
                _('Post method needs the data to be inserted.'
                  ' No data passed!'))
        if not isinstance(params, dict):
            raise AttributeError(
                _('Post method needs the data to be inserted.'
                  ' Invalid data passed!'))

        print(params)
        response = requests.post(resource, data=json.dumps(params),
                                 headers={'content-type': 'application/json'})
        # print(response.status_code, response.headers['content-type'])
        if response.status_code == 201:  # Success
            return response.text, None, response.status_code
        # Failure
        return None, response.text, response.status_code

    def put_method(self, resource, params):
        if (params is None) or (params == {}):
            raise AttributeError(
                _('Put method needs the data to be updated. No data passed!'))
        if not isinstance(params, dict):
            raise AttributeError(
                _('Put method needs the data to be updated.'
                  'Invalid data passed!'))
        _pk = params.pop('pk', None)
        if _pk is None:
            raise AttributeError(
                _('Put method needs the primary key. No primary key passed!'))
        response = requests.put(resource + '/%s' % _pk,
                                data=json.dumps(params),
                                headers={'content-type': 'application/json'})
        if response.status_code == 200:  # Success
            return response.text, None, response.status_code
        # Failure
        return None, response.text, response.status_code

    def delete_method(self, resource, params):
        _data = {}
        if params is None:
            pass
        elif isinstance(params, list):
            resource = resource + '%20'.join(params)
        elif isinstance(params, str):
            resource = resource + '/%s' % params
        elif isinstance(params, dict):
            _data = params

        response = requests.delete(resource, data=_data,
                                   headers={'content-type': 'application/json'})
        if response.status_code == 204:  # Success
            return response.text, None, response.status_code
        # Failure
        return None, response.text, response.status_code
