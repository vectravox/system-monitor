"""Application configuration constants."""

from pathlib import Path

"""Main window title."""
WINDOW_TITLE: str = "System Monitor"

"""Minimum window width in pixels."""
WINDOW_MIN_WIDTH: int = 800

"""Minimum window height in pixels."""
WINDOW_MIN_HEIGHT: int = 500

"""Default update interval for all data sources."""
UPDATE_INTERVAL_SECONDS: float = 2.0

"""Path to log file."""
DEFAULT_LOG_PATH: Path = Path("monitor.log")

"""Maximum time to wait for a thread to finish."""
THREAD_STOP_TIMEOUT_SECONDS: float = 2.0

"""Host to ping for network latency test."""
PING_HOST: str = "8.8.8.8"

"""Maximum time to wait for ping response."""
PING_TIMEOUT_SECONDS: float = 2.0

"""Path to binary file on USB device for sequential reading."""
USB_DATA_PATH: Path = Path("/media/usb/data.bin")

"""Number of bytes to read from USB file per update."""
USB_READ_SIZE_BYTES: int = 20

"""Possible sensor names to check for CPU temperature."""
TEMPERATURE_SENSORS: list[str] = ["coretemp", "k10temp", "cpu-thermal"]
