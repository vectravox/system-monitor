"""Ping data source."""

import logging
import subprocess

from src.domain.data_source import DataSource
from src.domain.models import DataSample
from src.infrastructure import config

logger = logging.getLogger(__name__)


class PingSource(DataSource):
    """Data source that pings a remote host and returns RTT.

    Uses subprocess to call `ping -c 1 <host>`.
    """

    @property
    def name(self) -> str:
        """Display name of the ping source."""
        return f"ping {self._host}"

    def __init__(self, host: str = config.PING_HOST) -> None:
        """Initialize ping source.

        Args:
            host: Host to ping, e.g. "8.8.8.8".

        """
        self._host = host
        self._timeout = config.PING_TIMEOUT_SECONDS
        logger.debug(f"PingSource initialized: {host}")

    def _parse_rtt(self, output: str) -> str | None:
        """Extract RTT from ping output."""
        for line in output.splitlines():
            if "time=" in line:
                return line.split("time=")[1].split(" ")[0]
        return None

    def fetch(self) -> DataSample:
        """Perform ping and return RTT.

        Returns:
            DataSample: Ping time in milliseconds.

        """
        try:
            result = subprocess.run(
                ["ping", "-c", "1", self._host],
                capture_output=True,
                text=True,
                timeout=self._timeout,
                check=False,
            )

            if result.returncode != 0:
                message = f"Ping to {self._host} failed: {result.stderr.strip()}"
                logger.warning(message)
                return self._make_error_sample(message)

            rtt = self._parse_rtt(result.stdout)
            if rtt is None:
                message = f"Could not parse ping output for {self._host}"
                logger.warning(message)
                return self._make_error_sample(message)

            return DataSample(
                source_name=self.name,
                value=rtt,
                unit="ms",
                status="OK",
            )

        except subprocess.TimeoutExpired:
            message = f"Ping to {self._host} timed out"
            logger.warning(message)
            return self._make_error_sample(message)
