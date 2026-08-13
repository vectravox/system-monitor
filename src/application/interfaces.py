"""Application layer interfaces."""

from typing import Protocol


class Monitor(Protocol):
    """Interface for the monitor service."""

    def start(self) -> None:
        """Start monitoring."""
        ...

    def stop(self) -> None:
        """Stop monitoring."""
        ...

    def is_running(self) -> bool:
        """Return whether monitoring is active."""
        ...
