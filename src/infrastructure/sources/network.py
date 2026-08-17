"""Network I/O data source."""

import time

import psutil

from src.domain.data_source import DataSource, DataSourceError
from src.domain.models import DataSample


class NetworkSource(DataSource):
    """Data source that reads network I/O speed.

    Uses psutil.net_io_counters() to calculate download/upload speed in KB/s.
    """

    def __init__(self) -> None:
        """Initialize network source."""
        self.name = "Сеть"

    def start(self) -> None:
        """Initialize network counters."""
        counters = self._read_net_io_counters()
        self._prev_time = time.time()
        self._prev_recv = counters.bytes_recv
        self._prev_sent = counters.bytes_sent

    def _read_net_io_counters(self) -> psutil._ntuples.snetio:
        """Read network I/O counters and raise error if unavailable."""
        counters = psutil.net_io_counters()
        if counters is None:
            raise DataSourceError("No network I/O counters available")
        return counters

    def _fetch_impl(self) -> DataSample:
        """Read network I/O speed."""
        counters = self._read_net_io_counters()
        now = time.time()
        recv_bytes = counters.bytes_recv
        sent_bytes = counters.bytes_sent

        # Calculate speed
        dt = now - self._prev_time
        recv_speed = (recv_bytes - self._prev_recv) / dt / 1024  # KB/s
        sent_speed = (sent_bytes - self._prev_sent) / dt / 1024  # KB/s

        self._prev_time = now
        self._prev_recv = recv_bytes
        self._prev_sent = sent_bytes

        return DataSample(
            source_name=self.name,
            value=f"Загрузка: {recv_speed:.1f} KB/s / Отправка: {sent_speed:.1f} KB/s",
            status="OK",
        )
