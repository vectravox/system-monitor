"""USB device data source."""

import logging
from pathlib import Path

from src.domain.data_source import DataSource, DataSourceError
from src.domain.models import DataSample
from src.infrastructure import config

logger = logging.getLogger(__name__)


class USBSource(DataSource):
    """Data source that reads a binary file from a USB device.

    Reads config.USB_READ_SIZE_BYTES bytes sequentially,
    wrapping around to the beginning at EOF.
    """

    def __init__(self, file_path: Path = config.USB_DATA_PATH) -> None:
        """Initialize USB source.

        Args:
            file_path: Path to binary file on USB device.

        Raises:
            FileNotFoundError: If USB file does not exist.

        """
        self._file_path = file_path
        self.name = f"USB ({self._file_path.name})"

    def open(self) -> None:
        """Open the USB file."""
        if not self._file_path.exists():
            raise FileNotFoundError(f"USB file not found: {self._file_path}")
        self._file = open(self._file_path, "rb")  # noqa: SIM115  # File kept open for performance
        logger.debug(f"USB file opened: {self._file_path}")

    def _fetch_impl(self) -> DataSample:
        """Read config.USB_READ_SIZE_BYTES bytes from USB file."""
        data = self._file.read(config.USB_READ_SIZE_BYTES)

        # If EOF, wrap around to beginning
        if not data:
            self._file.seek(0)
            data = self._file.read(config.USB_READ_SIZE_BYTES)

            if not data:
                raise DataSourceError(f"USB file is empty: {self._file_path}")

        hex_str = " ".join(f"{b:02x}" for b in data)

        return DataSample(
            source_name=self.name,
            value=hex_str,
            status="OK",
        )

    def close(self) -> None:
        """Close the USB file."""
        if self._file:
            self._file.close()
            logger.debug(f"USB file closed: {self._file_path}")
