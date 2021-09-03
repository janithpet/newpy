import logging
import logging.config
import os
import pathlib

from newpy.loggers import ColoredFormatter

print(str(pathlib.Path(__file__).parent.resolve()))
print(os.listdir(str(pathlib.Path(__file__).parent.resolve())))
logging.config.fileConfig(str(pathlib.Path(__file__).parent.resolve()) + "/logging_config.ini")
logger = logging.getLogger()
