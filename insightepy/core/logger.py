import traceback
from logging import getLogger

import coloredlogs
from coloredlogs import CAN_USE_BOLD_FONT

from insightepy import conf

LOG_LEVEL = conf.get_config('log', 'level')
FMT = '[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s'
DATE_FMT = '%Y-%m-%d %H:%M:%S'

# black, blue, cyan, green, magenta, red, white and yellow

FIELD_STYLES = dict(
    asctime=dict(color='black', bold=CAN_USE_BOLD_FONT),
    hostname=dict(color='blue'),
    levelname=dict(color='black', bold=CAN_USE_BOLD_FONT),
    programname=dict(color='cyan'),
    name=dict(color='magenta'))

LEVEL_STYLES = dict(
    spam=dict(color='green'),
    debug=dict(color='black', bold=CAN_USE_BOLD_FONT),
    verbose=dict(color='blue'),
    info=dict(color='blue'),
    notice=dict(color='orange'),
    warning=dict(color='yellow'),
    success=dict(color='green', bold=CAN_USE_BOLD_FONT),
    error=dict(color='red'),
    critical=dict(color='red', bold=CAN_USE_BOLD_FONT))


class Logger(object):
    def __init__(self, name):
        self._logger = getLogger(name)
        # custom color to logs
        coloredlogs.install(
            level=LOG_LEVEL,
            fmt=FMT,
            datefmt=DATE_FMT,
            level_styles=LEVEL_STYLES,
            field_styles=FIELD_STYLES,
            logger=self._logger,
        )

    def debug(self, msg): self._logger.debug(msg)

    def info(self, msg): self._logger.info(msg)

    def warn(self, msg): self._logger.warn(msg)

    def error(self, msg):
        self._logger.error('{} stack='.format(msg, traceback.format_exc()))
