from enum import Enum
import logging
from typing import Any


class TerminalColor(Enum):
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    GREEN = "\033[32m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    YELLOW = "\033[93m"
    RED = "\033[31m"
    BRIGHTRED = "\033[91m"
    BRIGHTWHITE = "\033[97m"

    def __str__(self) -> str:
        return self.value


class ColoredFormatter(logging.Formatter):
    FORMATS = {
        logging.DEBUG: f"{TerminalColor.BOLD}{TerminalColor.GREEN}",
        logging.ERROR: f"{TerminalColor.BOLD}{TerminalColor.RED}",
        logging.WARNING: f"{TerminalColor.BOLD}{TerminalColor.MAGENTA}",
        logging.CRITICAL: f"{TerminalColor.BOLD}{TerminalColor.BRIGHTRED}",
        logging.INFO: f"{TerminalColor.BOLD}{TerminalColor.BRIGHTWHITE}",
    }

    def __init__(
        self, fmt: str | None, datefmt: str | None, *args: Any, **kwargs: Any
    ) -> None:
        super().__init__(fmt, datefmt, *args, **kwargs)
        self.fmt = fmt

    def format(self, record: logging.LogRecord) -> str:
        record.levelname = (
            f"{self.FORMATS[record.levelno]}{record.levelname}{TerminalColor.ENDC}"
        )
        record.msg = f"{self.FORMATS[record.levelno]}{record.msg}{TerminalColor.ENDC}"

        return super().format(record)
