"""Random number data source using system entropy."""

import os

from src.domain.data_source import DataSource
from src.domain.models import DataSample
from src.infrastructure import config


class RandomSource(DataSource):
    """Data source that generates cryptographically secure random numbers.

    Uses os.urandom() which reads from /dev/urandom on Linux.
    This provides non-deterministic, unpredictable numbers based on
    system entropy collected by the kernel (hardware noise, timing jitter,
    device interrupts, etc.).
    """

    def __init__(self) -> None:
        """Initialize random source."""
        self.name = f"Случайное число, {config.RANDOM_NUMBER_BYTES} байт(а)"

    def fetch(self) -> DataSample:
        """Generate a cryptographically secure random number."""
        random_bytes = os.urandom(config.RANDOM_NUMBER_BYTES)
        value = int.from_bytes(random_bytes, byteorder="big")

        return DataSample(
            source_name=self.name,
            value=str(value),
            status="OK",
        )
