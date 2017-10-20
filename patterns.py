'''Configuration of the routes, or vocabulary of the bot'''
from botteryapp import app
from bottery.conf.patterns import Pattern, DefaultPattern
from bottery.views import pong
from cli_talker.views import (END_HOOK_LIST, flask_restless_view, help_text,
                              say_help, tec_view)


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


hang_user_pattern = HangUserPattern(flask_restless_view)

hang_user_pattern_tec = HangUserPattern(tec_view)

app.set_hang(hang_user_pattern, 'person')
app.set_hang(hang_user_pattern_tec, 'tec')

patterns = [
    hang_user_pattern,
    hang_user_pattern_tec,
    Pattern('tec', tec_view),
    Pattern('person', flask_restless_view),
    Pattern('ping', pong),
    Pattern('help', help_text),
    DefaultPattern(say_help)
]
