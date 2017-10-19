'''Configuration of the routes, or vocabulary of the bot'''
from bottery.conf.patterns import Pattern, DefaultPattern
from bottery.views import pong
from views import help_text, say_help, END_HOOK_LIST, two_tokens, \
    URL_APP


rules = {'tec': {'rank': URL_APP + '_rank?words=',
                 'filtra': URL_APP + '_filter_documents?afilter=',
                 'capitulo': URL_APP + '_document_content/',
                 '_message': 'Informe o comandocd .: '
                 }
         }
#                         'log': URL_APP + '_lacre/log',

rules_lacre = {'lacre': {'ll': URL_APP + '_lacre/lacre/',
                         'cc': URL_APP + '_lacre/container/',
                         '_message': 'Escolha uma das opções: '
                         }
               }

rules_cep = {'cep': {'busca': 'http://api.postmon.com.br/v1/cep/',
                     '_message': 'Informe o comando: '
                     }
             }

patterns = [
    Pattern('ping', pong),
    Pattern('help', help_text),
    DefaultPattern(say_help)
]
