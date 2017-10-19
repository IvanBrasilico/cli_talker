'''Configuration of the routes, or vocabulary of the bot'''
from botteryapp import app
from bottery.conf.patterns import Pattern, DefaultPattern
from bottery.views import pong
from cli_talker.views import (END_HOOK_LIST, help_text, interactive,
                              say_help, two_tokens)


class HangUserPattern(DefaultPattern):
    def __init__(self, view):
        self.hanged_users = set()
        super().__init__(view)

    def activate_hang(self, message):
        self.hanged_users.add(message.user.id)

    def deactivate_hang(self, message):
        self.hanged_users.discard(message.user.id)

    def check(self, message):
        if message is None:
            return 'Empty message'
        if message.user.id in self.hanged_users:
            return self.view

hang_user_pattern = HangUserPattern(interactive)

app.set_hang(hang_user_pattern)

patterns = [
    hang_user_pattern,
    Pattern('tec', interactive),
    Pattern('ping', pong),
    Pattern('help', help_text),
    DefaultPattern(say_help)
]
