from strategies.output_strategy import OutputStrategy


class ConsoleOutputStrategy(OutputStrategy):
    """Concrete strategy — prints records to stdout."""

    def write(self, record: dict) -> None:
        fields = " | ".join(
            f"{k}: {v}" for k, v in record.items() if str(v).strip()
        )
        print(fields)
