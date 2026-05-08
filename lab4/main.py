#!/usr/bin/env python3
"""
Lab 4 — Strategy pattern for data output.

Output strategy is selected from config.json — no code changes needed
to switch between console / Kafka / Redis.

Usage:
    python main.py
    python main.py --config config.json
"""
import argparse
import json
import sys
from pathlib import Path

from context import DataOutputContext
from reader.data_reader import CSVDataReader
from strategies.output_strategy import OutputStrategy


def _build_strategy(config: dict) -> OutputStrategy:
    name = config["output_strategy"]

    if name == "console":
        from strategies.console_strategy import ConsoleOutputStrategy
        return ConsoleOutputStrategy()

    if name == "kafka":
        from strategies.kafka_strategy import KafkaOutputStrategy
        return KafkaOutputStrategy(config["kafka"])

    if name == "redis":
        from strategies.redis_strategy import RedisOutputStrategy
        return RedisOutputStrategy(config["redis"])

    print(f"ERROR: unknown strategy '{name}'. Choose: console | kafka | redis", file=sys.stderr)
    sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(description="Stream dataset records via a chosen strategy.")
    parser.add_argument("--config", default="config.json")
    args = parser.parse_args()

    with open(args.config, encoding="utf-8") as f:
        config = json.load(f)

    data_file = config["data_file"]
    if not Path(data_file).exists():
        print(
            f"ERROR: data file not found: {data_file}\n"
            "Run `python download_dataset.py` first.",
            file=sys.stderr,
        )
        sys.exit(1)

    strategy = _build_strategy(config)
    reader = CSVDataReader(data_file)
    context = DataOutputContext(strategy)

    limit = config.get("limit")
    print(f"Strategy : {config['output_strategy'].upper()}")
    print(f"File     : {data_file}")
    print(f"Limit    : {limit if limit else 'all'}")
    print("-" * 60)

    count = context.execute(reader, limit=limit)

    print("-" * 60)
    print(f"Done. Processed {count} records.")


if __name__ == "__main__":
    main()
