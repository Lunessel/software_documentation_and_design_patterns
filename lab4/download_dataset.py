#!/usr/bin/env python3
"""
Download Salt Lake City Police Cases 2016 from Utah Open Data (Socrata API).

Usage:
    python download_dataset.py
    python download_dataset.py --limit 2000 --output data/my_file.csv
"""
import argparse
import urllib.request
import ssl
from pathlib import Path

_API_URL = "https://opendata.utah.gov/resource/trgz-4r9d.csv"
_DEFAULT_OUTPUT = "data/slc_police_cases_2016.csv"
_DEFAULT_LIMIT = 5000


def download(limit: int, output: str) -> None:
    url = f"{_API_URL}?$limit={limit}&$order=:id"
    out = Path(output)
    out.parent.mkdir(parents=True, exist_ok=True)

    print(f"Downloading up to {limit} records from Utah Open Data...")
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, context=ctx) as response:
        out.write_bytes(response.read())

    row_count = out.read_text(encoding="utf-8").count("\n") - 1
    print(f"Saved {row_count} records -> {out}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Download SLC Police Cases 2016 dataset to CSV."
    )
    parser.add_argument("--output", default=_DEFAULT_OUTPUT)
    parser.add_argument("--limit", type=int, default=_DEFAULT_LIMIT)
    args = parser.parse_args()
    download(args.limit, args.output)


if __name__ == "__main__":
    main()
