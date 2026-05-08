import csv
from pathlib import Path
from typing import Iterator


class CSVDataReader:
    """Reads records from a CSV file. Separated from output logic."""

    def __init__(self, file_path: str) -> None:
        self._path = Path(file_path)

    def records(self, limit: int | None = None) -> Iterator[dict]:
        with open(self._path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                if limit is not None and i >= limit:
                    break
                yield dict(row)
