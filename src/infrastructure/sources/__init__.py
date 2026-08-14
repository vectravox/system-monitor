"""Concrete implementations of DataSource interface.

This module provides factory functions for creating all data sources.
"""

import logging

from src.domain.datasource import DataSource

from .ping import PingSource

logger = logging.getLogger(__name__)


def generate_sources_list() -> list[DataSource]:
    """Create and return a list of all data sources."""
    sources: list[DataSource] = [
        PingSource(),
        # TODO: TemperatureSource(),
        # TODO: MemorySource(),
        # TODO: FanSpeedSource(),
        # TODO: USBSource(),
        # TODO: DiskIOSource(),
        # TODO: CpuLoadSource(),
        # TODO: NetworkSource(),
        # TODO: RandomSource(),
        # TODO: DummySource(),
    ]
    logger.debug(f"Created {len(sources)} sources")
    return sources


__all__ = [
    "PingSource",
    "generate_sources_list",
]
