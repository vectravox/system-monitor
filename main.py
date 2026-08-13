"""Application entry point for the System Monitor.

This module initializes logging, creates the Qt application,
and launches the main window. Run this file directly to start
the system monitoring GUI.
"""

from src.infrastructure.logging_config import setup_logging


def main() -> None:
    """Launch the System Monitor application."""
    setup_logging()


if __name__ == "__main__":
    main()
