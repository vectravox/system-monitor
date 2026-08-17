"""Concrete implementations of DataSource interface.

This module provides factory functions for creating all data sources.
"""

from collections.abc import Callable

from src.domain.data_source import DataSource

from .binary import BinaryReadSource
from .cpu import CpuLoadSource
from .disk import DiskUsageSource
from .fan import FanSpeedSource
from .memory import MemoryUsageSource
from .mouse import MouseCursorPositionSource
from .network import NetworkSource
from .ping import PingSource
from .temperature import TemperatureSource

"""List of active monitoring sources."""
SOURCES: list[Callable[[], DataSource]] = [
    CpuLoadSource,
    TemperatureSource,
    FanSpeedSource,
    MemoryUsageSource,
    DiskUsageSource,
    PingSource,
    NetworkSource,
    MouseCursorPositionSource,
    BinaryReadSource,
    # TODO: RandomSource,
]
