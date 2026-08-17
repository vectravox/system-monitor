"""Memory usage data source."""

import logging

import psutil

from src.domain.data_source import DataSource
from src.domain.models import DataSample

logger = logging.getLogger(__name__)


class MemorySource(DataSource):
    """Data source that reads memory usage.

    Uses psutil.virtual_memory().
    """

    def __init__(self, name: str) -> None:
        """Initialize memory source."""
        self._name = name
        logger.debug("MemorySource initialized")

    def _fetch_impl(self) -> DataSample:
        """Read memory usage."""
        mem = psutil.virtual_memory()
        used_gb = mem.used / (1024**3)
        total_gb = mem.total / (1024**3)

        logger.debug(f"Memory: {used_gb:.2f} GB / {total_gb:.2f} GB")
        return DataSample(
            source_name=self.name,
            value=f"{used_gb:.2f} / {total_gb:.2f}",
            unit="GB",
            status="OK",
        )
