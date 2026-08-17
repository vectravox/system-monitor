"""Application configuration constants."""

from pathlib import Path

"""Main window settings."""
WINDOW_TITLE: str = "System Monitor"
WINDOW_MIN_WIDTH: int = 800
WINDOW_MIN_HEIGHT: int = 500

"""Logging settings."""
DEFAULT_LOG_PATH: Path = Path("monitor.log")
# CONSOLE_LOG_LEVEL: str = "INFO"
CONSOLE_LOG_LEVEL: str = "DEBUG"
FILE_LOG_LEVEL: str = "DEBUG"
LOG_MSG_FORMAT: str = (
    "%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s"
)
LOG_DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S"

"""Default update interval for all data sources."""
UPDATE_INTERVAL_SECONDS: float = 2.0

"""Maximum time to wait for a thread to finish."""
THREAD_STOP_TIMEOUT_SECONDS: float = 2.0

"""Ping source settings."""
PING_HOST: str = "8.8.8.8"
PING_TIMEOUT_SECONDS: float = 2.0

"""USB source settings."""
# USB_DATA_PATH: Path = Path("/media/usb/data.bin")
USB_DATA_PATH: Path = Path("/mnt/backup/backups/easyeffectsrc")
USB_READ_SIZE_BYTES: int = 200

"""Possible sensor names to check for CPU temperature."""
TEMPERATURE_SENSORS: list[str] = ["coretemp", "k10temp", "cpu-thermal"]
