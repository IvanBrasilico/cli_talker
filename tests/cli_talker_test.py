'''Unit Tests for the views inside bottery.views'''
from cli_talker.cli_talker import locate_next, process_parameters, talker

URL = 'test'
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


def test_locate_next():
    # Test examples configuration
    assert locate_next('person', RULES) == (RULES['person'], 1)
    returned_dict, level = locate_next('person insert', RULES)
    assert level == 2
    assert returned_dict['resource'] == 'test/api/person'
    assert returned_dict['method'] == 'POST'
    returned_dict, level = locate_next('person update', RULES)
    assert level == 2
    assert returned_dict['resource'] == 'test/api/person'
    assert returned_dict['method'] == 'PUT'
    returned_dict, level = locate_next('person list', RULES)
    assert level == 2
    assert returned_dict['resource'] == 'test/api/person'
    assert returned_dict['method'] == 'GET'
    assert locate_next('person not_exist_com', RULES) == ({}, 2)


def test_process_parameters():
    # Test examples configuration
    returned_dict, level = locate_next('person view', RULES)
    params = returned_dict['params']
    assert  params == [{'name': 'fk', 'required': True}]
    assert level == 2
    param_list, nrequired = process_parameters(params)
    assert param_list == ['fk']
    assert nrequired == 1


def test_talker():
    # Test examples configuration
    resp, stay = talker('person', RULES)
    assert stay is True
    assert resp.find('Enter command: ') == 0
    resp, stay = talker('person view', RULES)
    assert stay is True
    assert resp.find(_('Required parameters: ')) == 0
    resp, stay = talker('person borrow', RULES)
    assert stay is False
    assert resp.find(_('Unrecognized command, exiting...')) == 0
    resp, stay = talker('person view 1', RULES)
    assert stay is False
    assert isinstance(resp, dict)
