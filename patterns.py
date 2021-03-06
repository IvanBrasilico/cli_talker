'''Configuration of the routes, or vocabulary of the bot'''
from botteryapp import ch, ih
from bottery.conf.patterns import Pattern, DefaultPattern
from bottery.views import pong
from cli_talker.views import (flask_restless_view, help_text,
                              say_help, tec_view)
from sql_alchemy_view.views import input_example, note_view, notebook_view



class FunctionPattern(Pattern):
    '''Allows check to be made by an user-defined function'''

    def __init__(self, pattern, view, function):
        '''Pass any function that receives a string and
        returns True or False'''
        self.function = function
        super().__init__(pattern, view)

    def check(self, message):
        return self.function(self.pattern, message.text)


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
hang_user_pattern_notebook = HangUserPattern(notebook_view)
hang_user_pattern_note = HangUserPattern(note_view)
hang_user_pattern_input = HangUserPattern(input_example)

ch.set_hang(hang_user_pattern, 'person')
ch.set_hang(hang_user_pattern_tec, 'tec')
ch.set_hang(hang_user_pattern_notebook, 'notebook')
ch.set_hang(hang_user_pattern_note, 'note')
ih.set_hang(hang_user_pattern_input, 'project')


def first_word(pattern, text):
    words = text.split(' ')
    if words:
        return words[0] == pattern
    return False


patterns = [
    hang_user_pattern,
    hang_user_pattern_tec,
    hang_user_pattern_notebook,
    hang_user_pattern_note,
    hang_user_pattern_input,
    Pattern('tec', tec_view),
    Pattern('person', flask_restless_view),
    FunctionPattern('notebook', notebook_view, first_word),
    FunctionPattern('note', note_view, first_word),
    Pattern('project', input_example),
    Pattern('ping', pong),
    Pattern('help', help_text),
    DefaultPattern(say_help)
]
