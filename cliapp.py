import sys
from cli_talker.cli_talker import talker
from cli_talker.service_binder import Maitre, RESTWaiter
import cli_talker.localizations

URL = 'http://localhost:5000'

RULES = {'person':
         {'list': {'type': 'json_api',
                   'method': 'GET',
                   'resource': URL + '/api/person',
                   'params': None},
          'view': {'type': 'json_api',
                   'method': 'GET',
                   'resource': URL + '/api/person',
                   'params': [{'name': 'fk', 'required': True}]
                   },
          'insert': {'type': 'json_api',
                     'method': 'POST',
                     'resource': URL + '/api/person',
                     'params': [{'name': 'name', 'required': True},
                                {'name': 'birth_date', 'required': True}]
                     },
          'update': {'type': 'json_api',
                     'method': 'PUT',
                     'resource': URL + '/api/person',
                     'params': [{'name': 'fk', 'required': True},
                                {'name': 'name', 'required': True}]
                     },
          'delete': {'type': 'json_api',
                     'method': 'DELETE',
                     'resource': URL + '/api/person',
                     'params': [{'name': 'fk', 'required': True}]
                     },
          '_message': _('Enter command: ')
          }
         }

waiter = None
if len(sys.argv) > 1:
    type = sys.argv[1]
    if type == 'json':
        waiter = RESTWaiter()

word = ''
context = ''
while word != 'exit':
    print(_('Type any word or a sequence. Type "exit" to terminate'))
    word = input()
    context += ' ' + word
    print('context: ', context)
    response, stay = talker(context, RULES)
    if not stay:
        context = ''
    print('response:', response)
    if isinstance(response, dict) and waiter is not None:
        response = waiter.process_order(response)
    print('Remote response:', response)
