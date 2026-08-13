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
