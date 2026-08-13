"""Main window for the System Monitor application."""

import logging

from PySide6.QtWidgets import QMainWindow

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """Main window of the System Monitor application."""

    def __init__(self) -> None:
        """Initialize the main window."""
        super().__init__()
        self.setWindowTitle("System Monitor")
        self.setMinimumSize(800, 500)
        logger.info("MainWindow initialized")
