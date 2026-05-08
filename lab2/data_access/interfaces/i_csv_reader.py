from __future__ import annotations
from abc import ABC, abstractmethod


class ICSVReader(ABC):
    @abstractmethod
    def read(self, file_path: str) -> list[dict]:
        """Read CSV file and return list of row dicts."""
