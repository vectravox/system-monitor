"""Application entry point for the System Monitor.

This module initializes logging, creates the Qt application,
and launches the main window. Run this file directly to start
the system monitoring GUI.
"""

import sys

from PySide6.QtWidgets import QApplication

from src.application.monitor_service import MonitorService
from src.infrastructure.logging_config import setup_logging
from src.infrastructure.sources import generate_sources_list
from src.presentation.main_window import MainWindow


def main() -> None:
    """Launch the System Monitor application."""
    setup_logging()

    app = QApplication(sys.argv)

    sources = generate_sources_list()
    service = MonitorService(sources)

    window = MainWindow(service)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
