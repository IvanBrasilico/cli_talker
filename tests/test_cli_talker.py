'''Unit Tests for the views inside bottery.views'''
from cli_talker.cli_talker import (locate_next,
    process_parameters, talker)

RULES = {'book':
         {'list': '/list',
          'view': '/view/',
          'filter': '/filter',
          '_message': 'Enter command: '
          }
         }
PARAMS = {'filter:2':
          [{'name': 'author', 'required': True},
           {'name': 'name', 'required': True},
              {'name': 'publisher', 'required': False}
           ]}


def test_pong():
    assert pong('any_string') == 'pong'
    assert pong(1) == 'pong'
    assert pong(None) == 'pong'


def test_locate_next():
    # Test examples configuration
    assert locate_next('book', RULES) == (RULES['book'], 1)
    assert locate_next('book list', RULES) == ('/list', 2)
    assert locate_next('book not_exist_com', RULES) == ({}, 2)


def test_process_parameters():
    # Test examples configuration
    assert process_parameters('filter', 2, PARAMS) == \
        (['author', 'name', 'publisher'], 2)


@mock.patch('bottery.views.urlopen')
def test_call_api(urlopen):
    # Test examples configuration
    urlopen.return_value.read.return_value = '{"mocked": "mocked"}'
    message = type('Message', (object,), {'text': 'book'})
    resp, hook = access_api_rules(message, RULES)
    assert hook is True
    assert resp.find('Enter command:') == 0
    message.text = 'book view'
    assert access_api_rules(message, RULES) == ('Enter parameters: ', True)
    message.text = 'book view 1'
    assert access_api_rules(message, RULES) == ('mocked: mocked \n ', False)
