"""Abstract data source interface."""

from abc import ABC, abstractmethod

from .models import DataSample


class DataSource(ABC):
    """Abstract contract for all data sources.

    Every concrete source (PingSource, TemperatureSource, etc.)
    must implement the fetch() method.
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

        """
        ...
