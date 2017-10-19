# -*- coding: utf-8 -*-
'''Views customizadas utilizadas neste projeto
São as funcões que geram o conteúdo para a submissão à
API que o Usuário acessa.
'''
import json
from botteryapp import app
from cli_talker.cli_talker import talker
from cli_talker.service_binder import RESTWaiter
import rules

RULES = rules.RULES2
waiter = RESTWaiter()

URL_APP = 'http://brasilico.pythonanywhere.com/'
STATUS = ['OK', 'Divergente', 'Sem Lacre']
END_HOOK_LIST = ['fim', 'end', 'exit', 'sair']


def two_tokens(text):
    '''Receives a text string, splits on first space, return
    first word of list/original sentence and the rest of the sentence
    '''
    lista = text.split(' ')
    return lista[0], " ".join(lista[1:])


def help_text(message):
    '''Retorna a lista de Patterns/ disponíveis'''
    # TODO Fazer modo automatizado
    lstatus = [str(key) + ': ' + value + ' ' for key,
               value in list(enumerate(STATUS))]
    str_end_hook = ', '.join(END_HOOK_LIST)
    return ('help - esta tela de ajuda \n'
            'ping - teste, retorna "pong"\n'
            'person - entra na aplicação PERSON \n' +
            str_end_hook + ' - Sai de uma aplicação \n')


def say_help(message):
    '''Se comando não reconhecido'''
    return 'Não entendi o pedido. \n Digite help para uma lista de comandos.'


def interactive(message):
    app.hang_in(message)
    response, stay = talker(app.context[message.user.id], RULES)
    if not stay:
        app.hang_out(message)
    print('comando:', response)
    if isinstance(response, dict) and waiter is not None:
        response, error, status_code = waiter.process_order(response)
        #response = response.decode()
        print('Erro:', error, status_code)
        if error is None:
            response = clever_json2md(response)
        else:
            response = clever_json2md(error)
    print('Remote:', response, type(response))
    response = response.encode('utf8', 'replace')
    print(type(response), response)
    response = response.decode("utf-8", "replace")
    print(type(response), response)
    return response


def clever_json2md(response):
    try:
        json_response = json.loads(response)
    except json.JSONDecodeError:
        json_response = response
    str_response = ""
    if isinstance(json_response, list):
        for linha in json_response:
            if isinstance(linha, dict):
                print('list-dict')
                for key, value in linha.items():
                    str_response = str_response + \
                        key + ': ' + str(value) + ' \n '
            elif isinstance(linha, str):
                str_response = json_response
    elif isinstance(json_response, dict):
        print('dict')
        for key, value in json_response.items():
            str_response = str_response + key + ': ' + str(value) + ' \n '
    elif isinstance(json_response, str):
        print('STR***')
        str_response = json_response
    return str_response
