"""Mouse cursor position data source."""

from PySide6.QtGui import QCursor

from src.domain.data_source import DataSource
from src.domain.models import DataSample


class MouseCursorPositionSource(DataSource):
    """Data source that reads the current mouse cursor position.

    Uses PySide6.QtGui.QCursor to get X/Y coordinates.
    """

    update_interval = 1.0

    def __init__(self) -> None:
        """Initialize mouse cursor position source."""
        self.name = "Позиция курсора"

    def _fetch_impl(self) -> DataSample:
        """Read current mouse cursor position."""
        pos = QCursor.pos()
        return DataSample(
            source_name=self.name,
            value=f"X: {pos.x()} / Y: {pos.y()}",
            status="OK",
        )
