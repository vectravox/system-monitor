"""Logging configuration for the entire application."""

import logging
import sys
from pathlib import Path

_LOG_LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}


def setup_logging(
    log_file: str = "monitor.log",
    console_level: str = "INFO",
    file_level: str = "DEBUG",
) -> None:
    """Configure logging for the application.

    Logs are written to both console and a file.
    Console output: INFO and above (user-friendly).
    File output: DEBUG and above (detailed for debugging).

    Args:
        log_file: Path to the log file (default: "monitor.log").
        console_level: Log level for console output (default: "INFO").
        file_level: Log level for file output (default: "DEBUG").

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

    log_format = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(console_level_num)
    console_handler.setFormatter(log_format)
    root_logger.addHandler(console_handler)

    log_path = Path(log_file)
    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setLevel(file_level_num)
    file_handler.setFormatter(log_format)
    root_logger.addHandler(file_handler)

    # Log startup message
    logger = logging.getLogger(__name__)
    logger.info(f"Logging initialized. File: {log_path.absolute()}")
    logger.debug("Debug logging enabled")
