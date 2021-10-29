import logging
import logging.config
import pathlib

from newpy.loggers import ColoredFormatter

logging.config.fileConfig(str(pathlib.Path(__file__).parent.resolve()) + "/logging_config.ini")
logger = logging.getLogger()
