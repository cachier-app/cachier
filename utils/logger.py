
from rich.console import Console
from rich.syntax import Syntax

import logging
from rich.logging import RichHandler

FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)
log = logging.getLogger("rich")


class Logger:
    def __init__(self, debugEnabled=False):
        self.debug = debugEnabled

    def logme(self, message, type=None):
        if type=='info':
            logging.info(message, extra={"markup": True})
        elif type=='debug':
            logging.debug(message, extra={"markup": True})
        elif type=='warning':
            logging.warning(message, extra={"markup": True})
        elif type=='error':
            logging.error(message, extra={"markup": True})
        else:
            logging.info(message, extra={"markup": True})


    def debuglog(self, message, logType="INFO"):
        if not self.debug:
            return 
        logging.debug(f"{message} ({logType.upper()})", extra={"markup": True})
