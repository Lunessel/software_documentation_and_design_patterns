#!/usr/bin/env python3
"""Entry point — imports CSV data into the database.

Usage:
    python main.py
    python main.py --csv data/compensations.csv --db sqlite:///data/compensation.db
"""

import argparse
import sys

from container import Container

DEFAULT_CSV = "data/compensations.csv"
DEFAULT_DB = "sqlite:///data/compensation.db"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Load compensation data from CSV into the database."
    )
    parser.add_argument("--csv", default=DEFAULT_CSV, help="Path to input CSV file")
    parser.add_argument("--db", default=DEFAULT_DB, help="SQLAlchemy DB URL")
    args = parser.parse_args()

    container = Container(db_url=args.db)
    try:
        print(f"Loading data from: {args.csv}")
        container.import_service.import_from_csv(args.csv)
        print("Done.")
    except FileNotFoundError:
        print(
            f"ERROR: File not found: {args.csv}\n"
            "Run `python generate_csv.py` first to create the data file.",
            file=sys.stderr,
        )
        sys.exit(1)
    finally:
        container.close()


if __name__ == "__main__":
    main()
