"""CPU load data source."""

import psutil

from src.domain.data_source import DataSource
from src.domain.models import DataSample


class CpuLoadSource(DataSource):
    """Data source that reads CPU load percentage.

    Uses psutil.cpu_percent().
    """

    def __init__(self) -> None:
        """Initialize CPU load source."""
        self.name = "Загрузка CPU"

    def fetch(self) -> DataSample:
        """Read CPU load percentage."""
        load = psutil.cpu_percent(interval=0.1)

        return DataSample(
            source_name=self.name,
            value=f"{load:.1f}",
            unit="%",
            status="OK",
        )
