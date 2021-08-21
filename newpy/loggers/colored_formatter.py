import logging

from humanfriendly.terminal import ansi_wrap


class ColoredFormatter(logging.Formatter):
	FORMATS = {
		logging.DEBUG: {"color": "green", "bold": True},
		logging.ERROR: {"color": "red", "bold": True},
		logging.WARNING: {"color": "yellow", "bold": True},
		logging.CRITICAL: {"color": "magenta", "bright": True, "bold": True},
		logging.INFO: {"color": "white", "bold": True}
	}

	def __init__(self, fmt, datefmt, *args, **kwargs):
		super().__init__(fmt, datefmt, *args, **kwargs)
		self.fmt = fmt

	def format(self, record):
		record.levelname = ansi_wrap(record.levelname, **self.FORMATS[record.levelno])
		record.msg = ansi_wrap(str(record.msg), **self.FORMATS[record.levelno])
		return super().format(record)
