from reader.data_reader import CSVDataReader
from strategies.output_strategy import OutputStrategy


class DataOutputContext:
    """
    Strategy context.

    Knows HOW to iterate and delegate to a strategy,
    but does not know WHICH strategy is used.
    """

    def __init__(self, strategy: OutputStrategy) -> None:
        self._strategy = strategy

    def set_strategy(self, strategy: OutputStrategy) -> None:
        self._strategy = strategy

    def execute(self, reader: CSVDataReader, limit: int | None = None) -> int:
        self._strategy.open()
        count = 0
        try:
            for record in reader.records(limit):
                self._strategy.write(record)
                count += 1
        finally:
            self._strategy.close()
        return count
