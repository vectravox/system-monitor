"""Monitor service implementation."""

import logging

from src.domain.datasource import DataSource
from src.domain.models import DataSample

logger = logging.getLogger(__name__)


class MonitorService:
    """Service for controlling the monitoring process."""

    def __init__(self, sources: list[DataSource]) -> None:
        """Initialize the monitor service with monitoring stopped."""
        self.is_running: bool = False
        self.sources = sources
        logger.debug("MonitorService initialized")

    def start(self) -> None:
        """Start monitoring."""
        if self.is_running:
            logger.warning("Monitoring already running")
            return
        self.is_running = True
        logger.info("Monitoring started")

    def stop(self) -> None:
        """Stop monitoring."""
        if not self.is_running:
            logger.warning("Monitoring already stopped")
            return
        self.is_running = False
        logger.info("Monitoring stopped")

    def fetch(self) -> list[DataSample]:
        """Fetch data from all sources."""
        if self.is_running:
            return [source.fetch() for source in self.sources]
        else:
            raise RuntimeError("Trying to fetch data from stopped monitoring service")
