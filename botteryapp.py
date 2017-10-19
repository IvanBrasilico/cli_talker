import logging.config
from bottery.app import App
from bottery.log import DEFAULT_LOGGING

logging.config.dictConfig(DEFAULT_LOGGING)
logger = logging.getLogger('bottery')
logger.setLevel(logging.DEBUG)

app = App()
app.run()