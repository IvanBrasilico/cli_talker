from collections import OrderedDict
import logging.config
from bottery.app import App
from bottery.conf.patterns import Pattern, DefaultPattern
from bottery.log import DEFAULT_LOGGING
import cli_talker.localizations


class ContextApp(App):
    def __init__(self):
        self.context = dict()
        self.hang = dict()
        self.input_queue = dict()
        self.user_session = dict()
        super().__init__()

    def set_hang(self, hang, hang_pattern):
        self.hang[hang_pattern] = hang

    def hang_in(self, message):
        self.user_session[message.user.id] = dict()
        usercontext = self.context.get(message.user.id, '')
        usercontext += message.text.strip() + ' '
        self.context[message.user.id] = usercontext
        first_word = usercontext.split(' ')[0]
        self.hang[first_word].activate_hang(message)
        return usercontext

    def hang_out(self, message):
        first_word = self.context[message.user.id].split(' ')[0]
        self.hang[first_word].deactivate_hang(message)
        self.context.pop(message.user.id, None)
        self.user_session.pop(message.user.id, None)

    def input(self, message, name, prompt, valid_values=None):
        if not self.input_queue.get(message.user.id, None):
            self.input_queue[message.user.id] = OrderedDict()
        self.user_session[message.user.id] = dict()
        user_input_dict = self.input_queue[message.user.id]
        user_input_dict[name] = (prompt, valid_values)

    def print_next_input(self, message):
        user_input_dict = self.input_queue[message.user.id]
        if not user_input_dict:
            return _('No messages on the input command queue')

        actual_prompt, _valid_values = list(user_input_dict.values())[0]
        print(actual_prompt)
        return actual_prompt

    def next_input_queue(self, message):
        user_input_dict = self.input_queue[message.user.id]
        if not user_input_dict:
            return False, _('No messages on the input command queue')

        _actual_prompt, valid_values = list(user_input_dict.values())[0]
        if valid_values:
            if message.text not in valid_values:
                return True, _('Enter a Valid Value: ' + ' '.join(valid_values))

        usercontext = self.context.get(message.user.id, '')
        usercontext += message.text.strip() + ' '
        self.context[message.user.id] = usercontext
        user_session = self.user_session[message.user.id]
        name = list(user_input_dict.keys())[0]
        user_session[name] = message.text
        user_input_dict.popitem(last=False)
        if not user_input_dict:
            return False, ' '.join('{}:{}'.format(key, val) for key, val in user_session.items())

        next_prompt, valid_values = list(user_input_dict.values())[0]
        if valid_values:
                next_prompt = next_prompt + ' - ' + ' '.join(valid_values)
        return True, next_prompt


app=ContextApp()


if __name__ == '__main__':
    logging.config.dictConfig(DEFAULT_LOGGING)
    logger=logging.getLogger('bottery')
    logger.setLevel(logging.DEBUG)

    app.run()
