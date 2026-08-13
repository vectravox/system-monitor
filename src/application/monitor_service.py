"""Monitor service implementation."""

import logging

logger = logging.getLogger(__name__)


class MonitorService:
    """Service for controlling the monitoring process."""

    def __init__(self) -> None:
        """Initialize the monitor service with monitoring stopped."""
        self._running: bool = False
        logger.debug("MonitorService initialized")

    def start(self) -> None:
        """Start monitoring."""
        if self._running:
            logger.warning("Monitoring already running")
            return
        self._running = True
        logger.info("Monitoring started")

    def stop(self) -> None:
        """Stop monitoring."""
        if not self._running:
            logger.warning("Monitoring already stopped")
            return
        self._running = False
        logger.info("Monitoring stopped")

    def is_running(self) -> bool:
        """Check whether monitoring is currently active."""
        return self._running
