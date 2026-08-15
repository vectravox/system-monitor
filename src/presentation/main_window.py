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

from src.application.monitor_service import MonitorService
from src.domain.models import DataSample
from src.infrastructure import config

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """Main window of the System Monitor application."""

    def __init__(self, service: MonitorService) -> None:
        """Initialize the main window.

        Args:
            service: Monitor service instance.

        """
        super().__init__()
        self.service = service
        self.service.data_ready.connect(self.update_table_row)
        self.rows = len(self.service.sources)
        self.setup_ui()
        logger.debug("MainWindow initialized")

    def setup_ui(self) -> None:
        """Create and arrange all UI components."""
        self.setWindowTitle(config.WINDOW_TITLE)
        self.setMinimumSize(config.WINDOW_MIN_WIDTH, config.WINDOW_MIN_HEIGHT)

        # Button
        self.start_stop_button = QPushButton("Старт")
        self.start_stop_button.clicked.connect(self.on_start_stop_clicked)

        # Table model
        self.table_model = QStandardItemModel()
        self.table_model.setHorizontalHeaderLabels(["Источник", "Данные"])

        # Inital items
        for row in range(self.rows):
            self.table_model.setItem(
                row, 0, QStandardItem(self.service.sources[row].name)
            )
            self.table_model.setItem(row, 1, QStandardItem("Ожидание запуска..."))

        # Table view
        self.table = QTableView()
        self.table.setSelectionMode(QTableView.SelectionMode.NoSelection)
        self.table.setEditTriggers(QTableView.EditTrigger.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setModel(self.table_model)
        self.table.resizeColumnToContents(0)

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
        if not self.service.is_running:
            self.service.start()
            self.start_stop_button.setText("Стоп")
        else:
            self.service.stop()
            self.start_stop_button.setText("Старт")

    @Slot(int, DataSample)
    def update_table_row(self, row: int, sample: DataSample) -> None:
        """Update table row with data from source."""
        data_item = QStandardItem()
        display_text = sample.value

        if sample.status == "OK":
            data_item.setForeground(Qt.GlobalColor.black)
            if sample.unit:
                display_text = f"{display_text} {sample.unit}"
        elif sample.status == "ERROR":
            data_item.setForeground(Qt.GlobalColor.red)
            display_text = f"ERROR: {display_text}"

        data_item.setText(display_text)

        self.table_model.setItem(row, 0, QStandardItem(sample.source_name))
        self.table_model.setItem(row, 1, data_item)
        self.table.resizeColumnToContents(0)
