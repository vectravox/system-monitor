"""Abstract data source interface."""

from abc import ABC, abstractmethod

from .models import DataSample


class DataSourceError(Exception):
    """Base exception for all data source errors.

    Raised when a data source fails to collect data.
    """


class DataSource(ABC):
    """Abstract contract for all data sources.

    Each concrete implementation provides logic for collecting
    a specific system metric (CPU, memory, ping, etc.).
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Display name of the data source."""
        ...

    @abstractmethod
    def fetch(self) -> DataSample:
        """Collect a single measurement from the source.

        Returns:
            DataSample: Measurement data.

        Raises:
            DataSourceError: If the source is unavailable or data cannot be read.
            PermissionError: If the process lacks necessary permissions.
            FileNotFoundError: If a required file or device is missing.
            OSError: If a system call fails.

        """
        ...

    def _make_error_sample(self, message: str) -> DataSample:
        """Create an error DataSample with logging.

        Args:
            message: Error description.

        Returns:
            DataSample with status="ERROR".

        """
        return DataSample(
            source_name=self.name,
            value=message,
            status="ERROR",
        )
