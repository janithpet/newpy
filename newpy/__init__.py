import logging
import logging.config
import os
import pathlib

from newpy.loggers import ColoredFormatter

logging.config.fileConfig(str(pathlib.Path(__file__).parent.parent.resolve()) + "/logging_config.ini")
logger = logging.getLogger()
