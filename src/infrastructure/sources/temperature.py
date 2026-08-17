"""CPU temperature data source."""

import logging

import psutil

from src.domain.data_source import DataSource, DataSourceError
from src.domain.models import DataSample
from src.infrastructure import config

logger = logging.getLogger(__name__)


class TemperatureSource(DataSource):
    """Data source that reads CPU temperature.

    Uses psutil.sensors_temperatures().
    """

    def __init__(self) -> None:
        """Initialize temperature source."""
        self.name = "Температура CPU"

    def _fetch_impl(self) -> DataSample:
        """Read CPU temperature."""
        temps = psutil.sensors_temperatures()

        for sensor_name in config.TEMPERATURE_SENSORS:
            if sensor_name in temps:
                temp = temps[sensor_name][0].current
                return DataSample(
                    source_name=self.name,
                    value=f"{temp:.1f}",
                    unit="°C",
                    status="OK",
                )

        raise DataSourceError("No CPU temperature sensor found")
