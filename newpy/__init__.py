import logging
import logging.config
import os

from newpy.loggers import ColoredFormatter

logging.config.fileConfig(os.environ["LOGGING_CONFIG_PATH"])
logger = logging.getLogger()
