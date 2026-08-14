"""Application layer interfaces."""

from typing import Protocol

from src.domain.datasource import DataSource
from src.domain.models import DataSample


class Monitor(Protocol):
    """Interface for the monitor service."""

    sources: list[DataSource]
    is_running: bool

    def start(self) -> None:
        """Start monitoring."""
        ...

    def stop(self) -> None:
        """Stop monitoring."""
        ...

    def fetch(self) -> list[DataSample]:
        """Get data from sources."""
        ...
