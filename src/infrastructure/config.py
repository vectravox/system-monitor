"""Application configuration constants."""

from pathlib import Path

"""Main window settings."""
WINDOW_TITLE: str = "System Monitor"
WINDOW_MIN_WIDTH: int = 800
WINDOW_MIN_HEIGHT: int = 500

"""Logging settings."""
DEFAULT_LOG_PATH: Path = Path("monitor.log")
CONSOLE_LOG_LEVEL: str = "INFO"
FILE_LOG_LEVEL: str = "DEBUG"
LOG_MSG_FORMAT: str = (
    "%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s"
)
LOG_DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S"

"""Default update interval for all data sources."""
DEFAULT_UPDATE_INTERVAL_SECONDS: float = 2.0

"""Custom update interval for different data sources."""
CUSTOM_UPDATE_INTERVALS_SECONDS: dict[str, float] = {
    "MouseCursorPositionSource": 0.1,
}

"""Maximum time to wait for a Qt thread to finish."""
THREAD_STOP_TIMEOUT_SECONDS: float = 2.0

"""Ping source settings."""
PING_HOST: str = "8.8.8.8"
PING_TIMEOUT_SECONDS: float = 2.0

"""Binary source settings."""
BINARY_DATA_PATH: Path = Path("/media/usb/data.bin")
BINARY_READ_SIZE_BYTES: int = 20

"""Possible sensor names to check for CPU temperature."""
TEMPERATURE_SENSORS: list[str] = ["coretemp", "k10temp", "cpu-thermal"]

"""Number of random bytes used to generate an integer."""
RANDOM_NUMBER_BYTES = 2
