"""Disk usage data source."""

import psutil

from src.domain.data_source import DataSource
from src.domain.models import DataSample


class DiskUsageSource(DataSource):
    """Data source that reads disk usage.

    Uses psutil.disk_usage('/') to show used space in GB and percentage.
    """

    def __init__(self) -> None:
        """Initialize disk usage source."""
        self.name = "Использование диска"

    def _fetch_impl(self) -> DataSample:
        """Read disk usage."""
        usage = psutil.disk_usage("/")
        used_gb = usage.used / (1024**3)
        total_gb = usage.total / (1024**3)
        percent = usage.percent

        return DataSample(
            source_name=self.name,
            value=f"{used_gb:.1f} / {total_gb:.1f} GB ({percent:.0f}%)",
            status="OK",
        )
