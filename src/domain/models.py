from dataclasses import dataclass


@dataclass(frozen=True)
class DataSample:
    source_name: str
    value: str
    unit: str | None = None
    status: str

    def __post_init__(self):
        if not self.source_name or not self.source_name.strip():
            raise ValueError("source_name cannot be empty")
        if self.value is None:
            raise ValueError("value cannot be None")
        if self.status not in ("OK", "ERROR"):
            raise ValueError(f"Invalid status: {self.status}")
        if self.unit is not None and not self.unit.strip():
            raise ValueError("unit cannot be empty string")
