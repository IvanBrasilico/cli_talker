URL = 'http://localhost:5000'

RULES = {'person':
         {'list': {'type': 'json_api',
                   'method': 'GET',
                   'resource': URL + '/api/person',
                   'params': None},
          'view': {'type': 'json_api',
                   'method': 'GET',
                   'resource': URL + '/api/person',
                   'params': [{'name': 'pk', 'required': True}]
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
                     'params': [{'name': 'pk', 'required': True},
                                {'name': 'name', 'required': True}]
                     },
          'delete': {'type': 'json_api',
                     'method': 'DELETE',
                     'resource': URL + '/api/person',
                     'params': [{'name': 'pk', 'required': True}]
                     },
          '_message': _('Enter command: ')
          }
         }

RULES2 = {'tec':
          {'filter': {'type': 'json_api',
                      'method': 'GET',
                      'resource': URL + '/_filter_documents',
                      'params': [{'name': 'afilter', 'required': True}],
                      },
           'rank': {'type': 'json_api',
                    'method': 'GET',
                    'resource': URL + '/_rank',
                    'params': [{'name': 'words', 'required': True}]
                    },
           '_message': _('Enter command: ')
           }
          }
