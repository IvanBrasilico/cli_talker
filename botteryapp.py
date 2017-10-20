import logging.config
from bottery.app import App
from bottery.conf.patterns import Pattern, DefaultPattern
from bottery.log import DEFAULT_LOGGING
import cli_talker.localizations


class ContextApp(App):
    def __init__(self):
        self.context = dict()
        self.hang = dict()
        super().__init__()

    def set_hang(self, hang, hang_pattern):
        self.hang[hang_pattern] = hang

    def hang_in(self, message):
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


app = ContextApp()


if __name__ == '__main__':
    logging.config.dictConfig(DEFAULT_LOGGING)
    logger = logging.getLogger('bottery')
    logger.setLevel(logging.DEBUG)

    app.run()
