import sys
from cli_talker.cli_talker import talker
from cli_talker.service_binder import Maitre, RESTWaiter
import cli_talker.localizations
import rules

RULES = rules.RULES

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
