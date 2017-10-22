'''A String parser that can do a CLI like style conversation
For CLI, it means: list of commands + list of parameters
The flow maps a sequence of words to actions.
When the list is incomplete, the "bot" asks for next information
For rule-based bots that needs to interact with an API or a DataBase
'''
import shlex
import sys

import cli_talker.localizations


def locate_next(words, rules, level=1):
    '''Recursively process the rule chain against words until
    key 'resource' is find OR words ends
    Used by talker'''
    try:
        # alist = words.split(' ')
        # (like in shell, preserves expressions in quotes)
        alist = shlex.split(words)
        next_level = {}
        order = None
        for key, value in rules.items():
            if key == alist[0]:
                # print('key found =', alist[0])
                if isinstance(value, dict):
                    resource = value.get('resource')
                    if resource is None:
                        for k, v in value.items():
                            next_level[k] = v
                    else:
                        order = value

        if order is not None:
            # RESOURCE key found!!!
            return order, level
        else:
            if len(alist) > 1:
                # Nothing! Go process next word
                return locate_next(' '.join(alist[1:]),
                                   next_level, level + 1)
            # The end, return
            return next_level, level
    except AttributeError:
        print(_('Atribute error. Possibly misconfiguration of rules:'),
              sys.exc_info()[0])
        raise
    except:
        print(_('Unexpected error:'), sys.exc_info()[0])
        raise


def process_parameters(params):
    '''Process the parameter chain
    Used by talker
    Returns list of parameter names and number of
    parameters required'''
    if params is None:
        return None
    result = []
    n_required = 0
    for param in params:
        result.append(param['name'])
        if param['required'] is True:
            n_required += 1

    return result, n_required


def talker(text, rules):
    '''Interactive maps sequence of words to rules
    Rules(dict) map access to a resource (DB, ORM, API) throungh
    Returns two values:
     - message or resource: a feeedback to user or resource to access
     - stay flag (True or False)
    text: a phrase, a sequence of words by space passed by the Pattern object
    rules: a dict on format rules =
     {'command1': {'subcommand1':
        {'resource': 'url1',
            'method': '['GET' | 'POST' | 'PUT' | 'DELETE'],
            'params':
            [{'name': 'name1', 'required': True},
            {'name': 'name2', 'required': False}
            ],
'''
    # Splits like in shell: splits/tokenizes on spaces,
    # preserving expressions between quotes
    alist = shlex.split(text)
    # print(text)
    actual_level, level = locate_next(text, rules)
    if isinstance(actual_level, dict):
        if actual_level == {}:
            return _('Unrecognized command, exiting...'), False
        resource = actual_level.get('resource')
        if resource is None:
            local_dict = actual_level.copy()
            message = local_dict.pop('_message', '')
            return message + ' - '.join([key for key in local_dict]), True
    bind_params = {}
    params = actual_level.get('params')
    if params is not None:
        n_params_passed = len(alist) - level
        params_list, n_required = process_parameters(params)
        if n_params_passed < n_required:
            return _('Required parameters: ') + str(n_required) + \
                _(' Order: ') + ' '.join(params_list) + \
                _(' Number of parameters passed: ') + \
                str(n_params_passed), True
        # else n_params_passed >= n_required
        for name, value in zip(params, alist[level:]):
            # TEST if params are NAMED, else, try sequential binding
            index = value.find(name['name'] + '=')
            if index >= 0:
                name_value = value.split('=')
                bind_params[name_value[0]] = name_value[1]
            else:
                bind_params[name['name']] = value

    result_dict = actual_level.copy()
    result_dict['params'] = bind_params
    return result_dict, False
