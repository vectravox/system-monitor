"""Binary file data source."""

import logging
from pathlib import Path

from src.domain.data_source import DataSource, DataSourceError
from src.domain.models import DataSample
from src.infrastructure import config

logger = logging.getLogger(__name__)


class BinaryReadSource(DataSource):
    """Data source that reads a binary file.

    Reads config.BINARY_READ_SIZE_BYTES: bytes sequentially,
    wrapping around to the beginning at EOF.
    """

    def __init__(self, file_path: Path = config.BINARY_DATA_PATH) -> None:
        """Initialize binary data source.

        Args:
            file_path: Path to binary file.

        Raises:
            FileNotFoundError: If file does not exist.

        """
        self._file_path = file_path
        self.name = f"Чтение файла ({self._file_path.name})"

    def start(self) -> None:
        """Open the file."""
        if not self._file_path.exists():
            raise FileNotFoundError(f"File not found: {self._file_path}")
        self._file = open(self._file_path, "rb")  # noqa: SIM115  # File kept open for performance
        logger.debug(f"File for binary read opened: {self._file_path}")

    def stop(self) -> None:
        """Close the file."""
        if self._file:
            self._file.close()
            logger.debug(f"File for binary read closed: {self._file_path}")

    def fetch(self) -> DataSample:
        """Read config.BINARY_READ_SIZE_BYTES bytes from the file."""
        data = self._file.read(config.BINARY_READ_SIZE_BYTES)

        # If EOF, wrap around to beginning
        if not data:
            self._file.seek(0)
            data = self._file.read(config.BINARY_READ_SIZE_BYTES)

            if not data:
                raise DataSourceError(f"The file is empty: {self._file_path}")

        hex_str = " ".join(f"{b:02x}" for b in data)

        return DataSample(
            source_name=self.name,
            value=hex_str,
            status="OK",
        )
