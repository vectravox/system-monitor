"""Main window for the System Monitor application."""

import logging

from PySide6.QtWidgets import (
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from src.application.interfaces import Monitor

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """Main window of the System Monitor application."""

    def __init__(self, service: Monitor) -> None:
        """Initialize the main window.

        Args:
            service: Monitor service instance.

        """
        super().__init__()
        self._service = service
        self._setup_ui()
        logger.debug("MainWindow initialized")

    def _setup_ui(self) -> None:
        """Create and arrange all UI components."""
        self.setWindowTitle("System Monitor")
        self.setMinimumSize(800, 500)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self._start_stop_button = QPushButton("Старт")
        self._start_stop_button.clicked.connect(self._on_start_stop_clicked)
        layout.addWidget(self._start_stop_button)
        # layout.addStretch()

    def _on_start_stop_clicked(self) -> None:
        """Handle Start/Stop button click."""
        if not self._service.is_running():
            self._service.start()
            self._start_stop_button.setText("Стоп")
        else:
            self._service.stop()
            self._start_stop_button.setText("Старт")
