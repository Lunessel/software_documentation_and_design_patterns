#!/usr/bin/env python3
"""
Generate sample Salt Lake City Police Cases 2016 data.

Schema mirrors the real dataset at:
https://opendata.utah.gov/Public-Safety/SALT-LAKE-CITY-POLICE-CASES-2016/trgz-4r9d

Usage:
    python generate_sample_data.py
    python generate_sample_data.py --rows 2000 --output data/slc_police_cases_2016.csv
"""
import argparse
import csv
import random
from datetime import date, timedelta
from pathlib import Path

OFFENSE_TYPES = [
    "ASSAULT", "BURGLARY", "THEFT", "ROBBERY", "VANDALISM",
    "DRUG OFFENSE", "FRAUD", "TRESPASS", "DISORDERLY CONDUCT",
    "DUI", "WEAPONS OFFENSE", "DOMESTIC VIOLENCE", "ARSON",
    "MOTOR VEHICLE THEFT", "IDENTITY THEFT",
]

OFFENSE_GRADES = ["FELONY", "MISDEMEANOR", "INFRACTION"]

CLEARANCE_TYPES = [
    "ARREST", "UNFOUNDED", "EXCEPTIONAL", "OPEN", "CLOSED"
]

DISTRICTS = ["D1", "D2", "D3", "D4", "D5", "D6"]

STREETS = [
    "S STATE ST", "W TEMPLE", "N MAIN ST", "E BROADWAY",
    "S WEST TEMPLE", "W SOUTH TEMPLE", "N 300 W", "S 500 E",
    "W 900 S", "N 200 E", "S 1300 E", "W 2100 S",
]

FIELDNAMES = [
    "case_number", "report_date", "offense_date",
    "offense_code", "offense_type", "offense_grade",
    "address", "city", "state", "zip_code",
    "district", "grid_id",
    "clearance_code", "clearance_type", "clearance_date",
]


def _rand_date(year: int = 2016) -> str:
    start = date(year, 1, 1)
    return (start + timedelta(days=random.randint(0, 365))).isoformat()


def _generate_rows(n: int) -> list[dict]:
    rows = []
    for i in range(1, n + 1):
        offense_date = _rand_date()
        cleared = random.random() > 0.4
        rows.append({
            "case_number": f"16-{i:06d}",
            "report_date": offense_date,
            "offense_date": offense_date,
            "offense_code": f"{random.randint(100, 999)}",
            "offense_type": random.choice(OFFENSE_TYPES),
            "offense_grade": random.choice(OFFENSE_GRADES),
            "address": f"{random.randint(100, 9999)} {random.choice(STREETS)}",
            "city": "SALT LAKE CITY",
            "state": "UT",
            "zip_code": f"841{random.randint(0,9):02d}",
            "district": random.choice(DISTRICTS),
            "grid_id": f"{random.randint(1, 99):02d}{random.randint(0,9)}",
            "clearance_code": f"C{random.randint(1,9)}" if cleared else "",
            "clearance_type": random.choice(CLEARANCE_TYPES) if cleared else "OPEN",
            "clearance_date": _rand_date() if cleared else "",
        })
    return rows


def generate(output: str, rows: int) -> None:
    random.seed(42)
    out = Path(output)
    out.parent.mkdir(parents=True, exist_ok=True)

    data = _generate_rows(rows)
    with open(out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(data)

    print(f"Generated {rows} rows -> {out}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate sample SLC Police Cases 2016 CSV."
    )
    parser.add_argument("--output", default="data/slc_police_cases_2016.csv")
    parser.add_argument("--rows", type=int, default=1000)
    args = parser.parse_args()

    if args.rows < 1000:
        parser.error("--rows must be at least 1000")

    generate(args.output, args.rows)


if __name__ == "__main__":
    main()
