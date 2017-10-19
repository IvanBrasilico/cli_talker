import gettext
import locale

try:
    LOCALE, _E = locale.getdefaultlocale()
    language = gettext.translation('cli_talker', 'locale/', [LOCALE])
    language.install()
except FileNotFoundError:
    gettext.install('cli_talker')
