'''HOT Tests for Maitre and Waiter classes
Needs a running API. Using example from Flask-Restless
Just run python3 quickstart.py'''
import json
from cli_talker.service_binder import (Maitre, RESTWaiter)
import cli_talker.localizations

URL = 'http://localhost:5000'


maitre = Maitre()
maitre.add_waiter({'json_api': RESTWaiter})
order = {'type': 'json_api',
         'method': 'GET',
         'resource': URL + '/api/person',
         'params': None}
awaiter = maitre.process_order(order)

#r = requests.delete(URL + '/api/person/1', headers={'content-type': 'application/json'})

print('BEGIN HOT TEST - needs the Flask-Restless quickstart example running...')

newperson = {'name': u'Ivan', 'birth_date': '1975-12-17'}
print('POST:')
order['method'] = 'POST'
order['params'] = newperson
json_response, error, status_code = awaiter.process_order(order)
print(status_code)
print(json_response, error)
newid = json.loads(json_response)['id']
print('GET (id):')
order['method'] = 'GET'
order['params'] = {'pk': str(newid)}
json_response, error, status_code = awaiter.process_order(order)
print(status_code)
print(json_response, error)
print('PUT:')
newdata = {'pk': str(newid), 'name': u'Brasilico'}
order['method'] = 'PUT'
order['params'] = newdata
json_response, error, status_code = awaiter.process_order(order)
print(status_code)
print(json_response, error)
print('GET (no-id):')
order = {'type': 'json_api',
         'method': 'GET',
         'resource': URL + '/api/person'}
json_response, error, status_code = awaiter.process_order(order)
print(status_code)
print(json_response)
print('DELETE')
order['method'] = 'DELETE'
order['params'] = str(newid)
json_response, error, status_code = awaiter.process_order(order)
print(status_code)
print(json_response)
print('END')
