"""Main window for the System Monitor application."""

import logging

from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QCloseEvent, QKeySequence, QStandardItem, QStandardItemModel
from PySide6.QtWidgets import (
    QApplication,
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
        """Initialize the main window."""
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

        # Table
        self.table_model = self._create_table_model()
        self.table = self._create_table_view(self.table_model)

        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.central_widget_layout = QVBoxLayout(self.central_widget)

        # Add button and table to central widget
        self.central_widget_layout.addWidget(
            self.start_stop_button, alignment=Qt.AlignmentFlag.AlignLeft
        )
        self.central_widget_layout.addWidget(self.table)

    def _create_table_view(self, table_model: QStandardItemModel) -> QTableView:
        table = QTableView()
        table.setStyleSheet("""
            QTableView::item {
                padding: 5px;
            }
        """)
        table.setSelectionMode(QTableView.SelectionMode.NoSelection)
        table.setEditTriggers(QTableView.EditTrigger.NoEditTriggers)
        table.verticalHeader().setVisible(False)
        table.horizontalHeader().setStretchLastSection(True)
        table.setModel(self.table_model)
        table.resizeColumnToContents(0)
        table.resizeRowsToContents()
        return table

    def _create_table_model(self) -> QStandardItemModel:
        table_model = QStandardItemModel()
        table_model.setHorizontalHeaderLabels(["Источник", "Данные"])

        for row in range(self.rows):
            table_model.setItem(row, 0, QStandardItem(self.service.sources[row].name))
            table_model.setItem(row, 1, QStandardItem("Ожидание запуска..."))
        return table_model

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
        self.table.resizeRowToContents(row)

    def keyPressEvent(self, event) -> None:
        if event.matches(QKeySequence.StandardKey.Copy):
            self._copy_selected_cell()
        else:
            super().keyPressEvent(event)

    def _copy_selected_cell(self) -> None:
        index = self.table.currentIndex()
        if index.isValid():
            item = self.table_model.itemFromIndex(index)
            if item:
                QApplication.clipboard().setText(item.text())
                self.statusBar().showMessage("Текст скопирован ✅", 3500)

    def closeEvent(self, event: QCloseEvent) -> None:
        """Handle window close event."""
        if self.service.is_running:
            self.service.stop()
        event.accept()
        logger.debug("MainWindow closed")
