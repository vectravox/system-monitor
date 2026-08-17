"""Fan speed data source."""

import logging

import psutil

from src.domain.data_source import DataSource, DataSourceError
from src.domain.models import DataSample

logger = logging.getLogger(__name__)


class FanSpeedSource(DataSource):
    """Data source that reads fan speeds.

    Uses psutil.sensors_fans().
    """

    def __init__(self) -> None:
        """Initialize fan speed source."""
        self.name = "Скорость вентиляторов"

    def fetch(self) -> DataSample:
        """Read fan speeds.

        Returns:
            DataSample: All non-zero fan speeds in RPM (comma-separated list).

        """
        fans = psutil.sensors_fans()
        if not fans:
            raise DataSourceError("No fan sensors found")

        rpm_values: list[str] = []
        for fan_list in fans.values():
            for fan in fan_list:
                if fan.current > 0:
                    rpm_values.append(str(fan.current))

        if not rpm_values:
            raise DataSourceError("All fan speeds are zero (no active fans)")

        return DataSample(
            source_name=self.name,
            value=", ".join(rpm_values),
            unit="RPM",
            status="OK",
        )
