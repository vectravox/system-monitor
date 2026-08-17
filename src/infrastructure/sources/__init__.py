"""Concrete implementations of DataSource interface.

This module provides factory functions for creating all data sources.
"""

from collections.abc import Callable

from src.domain.data_source import DataSource

from .disk import DiskSource
from .fan import FanSpeedSource
from .memory import MemorySource
from .ping import PingSource
from .temperature import TemperatureSource
from .usb import USBSource

"""List of active monitoring sources."""
SOURCES: list[Callable[[], DataSource]] = [
    PingSource,
    TemperatureSource,
    MemorySource,
    FanSpeedSource,
    USBSource,
    DiskSource,
    # TODO: CpuLoadSource,
    # TODO: NetworkSource,
    # TODO: RandomSource,
    # TODO: DummySource,
]
