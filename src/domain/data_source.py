"""Abstract data source interface."""

import logging
from abc import ABC, abstractmethod
from collections.abc import Callable
from functools import wraps
from typing import ParamSpec

from .models import DataSample

logger = logging.getLogger(__name__)


class DataSourceError(Exception):
    """Error inside DataSource fetching logic."""


P = ParamSpec("P")


class DataSource(ABC):
    """Base class for all data sources.

    Subclasses implement fetch() to provide actual data collection.
    Optionally override start() and stop() for resource management.
    """

    name: str

    def catch_errors(
        self, func: Callable[P, DataSample | None]
    ) -> Callable[P, DataSample | None]:
        """Catch all unexpected errors.

        If the decorated method raises an exception, it is logged and
        a DataSample with status="ERROR" is returned.

        The wrapper intercepts exceptions and converts them into
        DataSample objects, ensuring that errors from any source
        are displayed in the GUI without crashing the application.
        """

        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> DataSample | None:
            try:
                return func(*args, **kwargs)
            except Exception as e:  # noqa: BLE001  # Intended
                error_msg = f'Failed to {func.__name__}: "{e}"'
                logger.warning(error_msg)
                return DataSample(
                    source_name=self.name,
                    value=error_msg,
                    status="ERROR",
                )

        return wrapper

    @abstractmethod
    def fetch(self) -> DataSample:
        """Implement data fetching from the source."""
        ...

    def start(self) -> None:  # noqa: B027
        """Prepare resources by the source. Override if needed."""

    def stop(self) -> None:  # noqa: B027
        """Release resources held by the source. Override if needed."""
