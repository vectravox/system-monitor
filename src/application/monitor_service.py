"""Monitor service implementation."""

import logging

from PySide6.QtCore import QObject, QThread, Signal, Slot

from src.application.data_fetcher import DataFetcher
from src.domain.data_source import DataSource
from src.domain.models import DataSample
from src.infrastructure import config

logger = logging.getLogger(__name__)


class MonitorService(QObject):
    """Service for controlling the monitoring process."""

    data_ready = Signal(int, DataSample)

    def __init__(self, sources: list[DataSource]) -> None:
        """Initialize the monitor service with sources."""
        super().__init__()
        self.is_running = False
        self.sources = sources
        self._threads: list[QThread] = []
        self._workers: list[DataFetcher] = []
        logger.debug(f"MonitorService initialized with {len(self.sources)} sources")

    def start(self) -> None:
        """Start monitoring all sources in background threads."""
        if self.is_running:
            logger.warning("Monitoring already running")
            return

        # Clean up any previous threads (safety)
        self._cleanup()

        logger.info(f"Starting monitoring for {len(self.sources)} sources")

        for row, source in enumerate(self.sources):
            thread = QThread()
            worker = DataFetcher(source)
            worker.moveToThread(thread)
            thread.started.connect(worker.run)

            # Forward data from fetcher to service, adding row number.
            # The row is captured in the lambda to preserve it for the callback.
            worker.data_ready.connect(
                lambda sample, row=row: self._on_data_ready(row, sample)
            )

            self._threads.append(thread)
            self._workers.append(worker)

            thread.start()
            logger.debug(f"Thread started for row {row}: {source.name}")

        self.is_running = True
        logger.info("Monitoring started")

    def stop(self) -> None:
        """Stop monitoring."""
        if not self.is_running:
            logger.warning("Monitoring already stopped")
            return

        logger.info(f"Stopping monitoring for {len(self._workers)} sources")

        for worker in self._workers:
            worker.stop()

        for thread in self._threads:
            thread.quit()
            thread.wait(
                int(config.THREAD_STOP_TIMEOUT_SECONDS * 1000)
            )  # Convert to milliseconds

        self._cleanup()
        self.is_running = False
        logger.info("Monitoring stopped")

    def _cleanup(self) -> None:
        """Clean up all thread and worker references."""
        self._workers.clear()
        self._threads.clear()
        logger.debug("Cleaned up threads and workers")

    @Slot(int, DataSample)
    def _on_data_ready(self, row: int, sample: DataSample) -> None:
        """Forward data from worker to GUI."""
        self.data_ready.emit(row, sample)
