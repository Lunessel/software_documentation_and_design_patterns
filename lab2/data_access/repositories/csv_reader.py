import csv

from data_access.interfaces.i_csv_reader import ICSVReader


class CSVReader(ICSVReader):
    def read(self, file_path: str) -> list[dict]:
        with open(file_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return [dict(row) for row in reader]
