"""Domain models (value objects) for the monitoring system."""

from dataclasses import dataclass


@dataclass(frozen=True)
class DataSample:
    """Immutable value object representing a single measurement.

    Attributes:
        source_name: Name of the data source (e.g., "CPU", "RAM").
        value: Measured value as string (e.g., "45.2", "1024").
        unit: Optional unit of measurement (e.g., "GB", "%", "ms").
        status: Status of the measurement ("OK" or "ERROR").

    """

    source_name: str
    value: str
    status: str
    unit: str | None = None

    def __post_init__(self) -> None:
        """Validate and normalize data after object creation.

        Raises:
            ValueError: If any field contains invalid data.

        """
        if not self.source_name or not self.source_name.strip():
            raise ValueError("source_name cannot be empty")

        if self.value is None:
            raise ValueError("value cannot be None")

        if self.status not in ("OK", "ERROR"):
            raise ValueError(f"Invalid status: {self.status}. Must be 'OK' or 'ERROR'")

        if self.unit is not None and not self.unit.strip():
            raise ValueError("unit cannot be empty string")
