"""Worker for running data sources in background threads."""

import logging

from PySide6.QtCore import QObject, QTimer, Signal, Slot

from src.domain.data_source import DataSource
from src.domain.models import DataSample

logger = logging.getLogger(__name__)


class DataFetcher(QObject):
    """Worker that periodically fetches data from a source in a background thread.

    Signals:
        data_ready: Emitted when new data is available (row, sample).
    """

    data_ready = Signal(DataSample)
    stop_requested = Signal()

    def __init__(
        self,
        source: DataSource,
        interval: float,
    ) -> None:
        """Initialize the worker."""
        super().__init__()
        self.stop_requested.connect(self._on_stop_requested)
        self.source = source
        self.interval = interval
        self.is_running = False
        self.timer: QTimer | None = None
        logger.debug(f"Worker created for {self.source.name}")

    @Slot()
    def run(self) -> None:
        """Start the worker loop."""
        if self.is_running:
            logger.warning(f'Worker for "{self.source.name}" is already running')
            return

        # Wrap source.start() with error handling.
        # In normal scenario source.start() doesn't return anything, but
        # if start() raises an exception, catch_errors returns a DataSample
        # with status="ERROR". We emit that error to the GUI and stop this worker.
        error_sample = self.source.catch_errors(self.source.start)()
        if error_sample:
            self.data_ready.emit(error_sample)
            return

        # Perform first fetch immediately to show data without waiting for timer.
        self._fetch_and_emit()

        # QTimer must be created in the thread where the fetcher lives.
        # Since the fetcher may be moved to a background QThread after creation,
        # the timer is created here (in run(), executed in that thread),
        # not in __init__() (executed in the main thread).
        self.timer = QTimer()
        self.timer.timeout.connect(self._fetch_and_emit)
        self.timer.setInterval(int(self.interval * 1000))  # Convert to milliseconds
        self.timer.start()

        self.is_running = True
        logger.debug(f'Worker started for "{self.source.name}"')

    def stop(self) -> None:
        """Stop the fetcher loop (called from any thread)."""
        self.stop_requested.emit()

    @Slot()
    def _on_stop_requested(self) -> None:
        """Handle stop request in the fetcher's thread."""
        if not self.is_running:
            logger.warning(f'Worker for "{self.source.name}" is already stopped')
            return

        if self.timer:
            self.timer.stop()
            self.timer.deleteLater()
            self.timer = None

        # Wrap source.stop() with error handling.
        # If stop() raises an exception, we emit the error DataSample to the GUI.
        error_sample = self.source.catch_errors(self.source.stop)()
        if error_sample:
            self.data_ready.emit(error_sample)

        self.is_running = False
        logger.debug(f'Worker stopped for "{self.source.name}"')

    @Slot()
    def _fetch_and_emit(self) -> None:
        """Fetch data from source and emit signals.

        This method is called by the timer every `interval` seconds.
        """
        # Wrap source.fetch() with error handling.
        # fetch() always returns a DataSample (either data or error).
        sample = self.source.catch_errors(self.source.fetch)()
        self.data_ready.emit(sample)
