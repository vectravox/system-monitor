"""Logging configuration for the entire application."""

import logging
import sys
from pathlib import Path
from typing import Literal

from . import config

_LOG_LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}


class ColoredFormatter(logging.Formatter):
    """Formatter with colors."""

    def __init__(
        self,
        fmt: str | None = None,
        datefmt: str | None = None,
        style: Literal["%", "{", "$"] = "%",
        use_colors: bool = True,
    ) -> None:
        """Initialize the colored formatter.

        Args:
            fmt: Log message format string.
            datefmt: Date/time format string.
            style: Format style ('%', '{', or '$').
            use_colors: Enable or disable all colors.

        """
        super().__init__(fmt, datefmt, style)
        self.COLORS = {
            "DEBUG": "\033[36m",  # Cyan
            "INFO": "\033[32m",  # Green
            "WARNING": "\033[33m",  # Yellow
            "ERROR": "\033[31m",  # Red
            "CRITICAL": "\033[35m",  # Magenta
            "RESET": "\033[0m",
        }
        self.use_colors = use_colors

    def format(self, record: logging.LogRecord) -> str:
        """Format the log record with optional ANSI colors."""
        orig_levelname = record.levelname
        orig_msg = record.msg

        if self.use_colors and record.levelname in self.COLORS:
            color = self.COLORS[record.levelname]
            reset = self.COLORS["RESET"]
            record.levelname = f"{color}{record.levelname}{reset}"

        formatted = super().format(record)

        record.levelname = orig_levelname
        record.msg = orig_msg
        return formatted


def setup_logging(
    log_file: Path = config.DEFAULT_LOG_PATH,
    console_level: str = config.CONSOLE_LOG_LEVEL,
    file_level: str = config.FILE_LOG_LEVEL,
    fmt: str = config.LOG_MSG_FORMAT,
    datefmt: str = config.LOG_DATE_FORMAT,
) -> None:
    """Configure logging for the application.

    Logs are written to both console and a file.
    Console default output: INFO and above (user-friendly).
    File default output: DEBUG and above (detailed for debugging).
    """
    try:
        console_level_num = _LOG_LEVELS[console_level.upper()]
        file_level_num = _LOG_LEVELS[file_level.upper()]
    except KeyError as e:
        raise ValueError(
            f"Invalid log level: {e}. Must be one of : {', '.join(_LOG_LEVELS.keys())}"
        ) from None

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    # Remove any existing handlers (to avoid duplicates)
    root_logger.handlers.clear()

    console_formatter = ColoredFormatter(fmt, datefmt, use_colors=True)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(console_level_num)
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)

    log_path = Path(log_file)
    file_formatter = ColoredFormatter(fmt, datefmt, use_colors=False)
    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setLevel(file_level_num)
    file_handler.setFormatter(file_formatter)
    root_logger.addHandler(file_handler)

    # Log startup message
    logger = logging.getLogger(__name__)
    logger.info(f"Logging initialized, logfile: {log_path.absolute()}")
    logger.debug("Debug logging enabled")
