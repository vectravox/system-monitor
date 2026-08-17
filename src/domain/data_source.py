"""Abstract data source interface."""

import logging
from abc import ABC, abstractmethod

from .models import DataSample

logger = logging.getLogger(__name__)


class DataSourceError(Exception):
    """Error inside DataSource fetching logic."""


class DataSource(ABC):
    """Base class for all data sources with built-in error handling.

    Subclasses implement _fetch_impl() to provide actual data collection.
    The public fetch() catches all exceptions and converts them to
    DataSample with status="ERROR", ensuring the application never crashes
    due to a failure in a single source.

    The name property returns self._name by default and can be overridden.
    """

    @property
    def name(self) -> str:
        """Display name of the data source.

        Used in the GUI table and error messages.

        Returns:
            str: Human-readable source name.
        """
        return self._name

    @abstractmethod
    def _fetch_impl(self) -> DataSample:
        """Implement actual data fetching logic.

        May raise exceptions. All exceptions are caught by fetch().
        """
        ...

    def fetch(self) -> DataSample:
        """Fetch data with automatic error handling.

        Returns:
            DataSample: status="OK" with data, or status="ERROR" with error message.
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
