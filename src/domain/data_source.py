"""Abstract data source interface."""

import logging
from abc import ABC, abstractmethod

from .models import DataSample

logger = logging.getLogger(__name__)


class DataSourceError(Exception):
    """Error inside DataSource fetching logic."""


class DataSource(ABC):
    """Abstract contract for all data sources.

    Each concrete implementation provides logic for collecting
    a specific system metric (CPU, memory, ping, etc.).
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Display name of the data source.

        Used in the GUI table and error messages.

        Returns:
            str: Human-readable source name.

        """
        ...

    @abstractmethod
    def _fetch_impl(self) -> DataSample:
        """Implement actual fetching logic.

        This method may raise exceptions. All exceptions are caught
        by the public fetch() method and converted to error DataSample.
        """
        ...

    def fetch(self) -> DataSample:
        """Public method to fetch data with automatic error handling.

        All exceptions from _do_fetch() are caught and logged.
        Instead of crashing, they are converted to DataSample with status="ERROR".
        This ensures that the application will not crash due to an unexpected
        failure in one of the data sources.

        Returns:
            DataSample: Either valid data (status="OK") or an error message (status="ERROR").

        """
        try:
            return self._fetch_impl()
        except Exception as e:  # noqa: BLE001
            error_msg = f'Failed to read: "{e}"'
            logger.warning(error_msg)
            return DataSample(
                source_name=self.name,
                value=error_msg,
                status="ERROR",
            )
