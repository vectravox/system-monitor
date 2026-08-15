"""Fan speed data source."""

import logging
import psutil

from src.domain.data_source import DataSource
from src.domain.models import DataSample

logger = logging.getLogger(__name__)


class FanSpeedSource(DataSource):
    """Data source that reads fan speeds.

    Uses psutil.sensors_fans().
    """

    @property
    def name(self) -> str:
        """Display name of the fan speed source."""
        return self._name

    def __init__(self) -> None:
        """Initialize fan speed source."""
        self._name = "Скорость вентиляторов"
        logger.debug("FanSpeedSource initialized")

    def fetch(self) -> DataSample:
        """Read fan speeds.

        Returns:
            DataSample: All non-zero fan speeds in RPM (comma-separated list).
        """
        fans = psutil.sensors_fans()
        if not fans:
            message = "No fan sensors found"
            logger.warning(message)
            return self._make_error_sample(message)

        rpm_values: list[str] = []
        for controller, fan_list in fans.items():
            for fan in fan_list:
                if fan.current > 0:
                    rpm_values.append(str(fan.current))

        if not rpm_values:
            message = "All fan speeds are zero (no active fans)"
            logger.warning(message)
            return self._make_error_sample(message)

        return DataSample(
            source_name=self.name,
            value=", ".join(rpm_values),
            unit="RPM",
            status="OK",
        )
