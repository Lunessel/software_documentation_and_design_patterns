from abc import ABC, abstractmethod


class OutputStrategy(ABC):
    """Abstract strategy — defines the interface for all output targets."""

    @abstractmethod
    def write(self, record: dict) -> None:
        """Write a single record to the target."""

    def open(self) -> None:
        """Set up connection/resources before writing starts."""

    def close(self) -> None:
        """Release connection/resources after writing ends."""
