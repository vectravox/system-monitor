"""Main window for the System Monitor application."""

import logging

from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QStandardItem, QStandardItemModel
from PySide6.QtWidgets import (
    QMainWindow,
    QPushButton,
    QTableView,
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
        self.service = service
        self.setup_ui()
        logger.debug("MainWindow initialized")

    def setup_ui(self) -> None:
        """Create and arrange all UI components."""
        self.setWindowTitle("System Monitor")
        self.setMinimumSize(800, 500)

        # Button
        self.start_stop_button = QPushButton("Старт")
        self.start_stop_button.clicked.connect(self.on_start_stop_clicked)

        # Table model
        self.table_model = QStandardItemModel(10, 2)
        self.table_model.setHorizontalHeaderLabels(["Источник", "Данные"])
        for row in range(10):
            self.table_model.setItem(row, 0, QStandardItem(f"Источник {row + 1}"))
            self.table_model.setItem(row, 1, QStandardItem("Ожидание запуска..."))

        # Table view
        self.table = QTableView()
        self.table.setSelectionMode(QTableView.SelectionMode.NoSelection)
        self.table.setEditTriggers(QTableView.EditTrigger.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setModel(self.table_model)

        # Create central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Add elements
        self.central_widget_layout = QVBoxLayout(self.central_widget)
        self.central_widget_layout.addWidget(
            self.start_stop_button, alignment=Qt.AlignmentFlag.AlignLeft
        )
        self.central_widget_layout.addWidget(self.table)

    @Slot()
    def on_start_stop_clicked(self) -> None:
        """Handle Start/Stop button click."""
        if not self.service.is_running():
            self.service.start()
            self.start_stop_button.setText("Стоп")
        else:
            self.service.stop()
            self.start_stop_button.setText("Старт")
