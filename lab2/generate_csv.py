#!/usr/bin/env python3
"""CLI module — generates a CSV data file with 1000+ compensation rows.

Usage:
    python generate_csv.py
    python generate_csv.py --output data/compensations.csv --rows 1050
"""

import argparse
import csv
import random
import uuid
from datetime import date, timedelta
from pathlib import Path

# ── seed data ──────────────────────────────────────────────────────────────────

FIRST_NAMES = [
    "Олексій", "Іван", "Марія", "Олена", "Андрій", "Тетяна", "Сергій", "Наталія",
    "Василь", "Людмила", "Михайло", "Оксана", "Павло", "Ірина", "Дмитро", "Галина",
    "Ярослав", "Юлія", "Богдан", "Вікторія", "Роман", "Алла", "Максим", "Лінa",
    "Євген", "Ганна", "Олег", "Світлана", "Денис", "Христина",
]

LAST_NAMES = [
    "Коваленко", "Бондаренко", "Ткаченко", "Кравченко", "Мельниченко",
    "Шевченко", "Іваненко", "Петренко", "Сидоренко", "Бойко",
    "Лисенко", "Гриценко", "Стець", "Мороз", "Олійник",
    "Заяць", "Лазаренко", "Федоренко", "Романенко", "Поліщук",
    "Марченко", "Тимченко", "Савченко", "Павленко", "Литвиненко",
]

POSITIONS = [
    "Software Engineer", "Senior Software Engineer", "Lead Engineer",
    "Project Manager", "Product Manager", "Business Analyst",
    "Data Analyst", "DevOps Engineer", "QA Engineer", "UX Designer",
    "Marketing Specialist", "HR Manager", "Finance Analyst", "Sales Manager",
    "System Architect", "Security Engineer", "Database Administrator",
]

CURRENCIES = ["UAH", "USD", "EUR"]

PAY_FREQUENCIES = ["WEEKLY", "BIWEEKLY", "MONTHLY", "ANNUALLY"]

TRIGGER_CRITERIA = [
    "Performance above 90%",
    "Sales target met",
    "Project completion on time",
    "Annual review bonus",
    "Quarterly target exceeded",
    "Team lead approval",
    "Customer satisfaction above 4.5",
    "Zero critical defects in quarter",
    "Successful product launch",
    "Client retention above 95%",
]

PLAN_NAMES = [
    "Standard Compensation Package",
    "Senior Employee Plan",
    "Executive Incentive Plan",
    "Tech Talent Retention",
    "Junior Developer Track",
    "Management Incentive Plan",
    "Performance-Based Package",
    "Annual Review Plan",
    "Remote Work Plan",
    "Hybrid Work Benefits",
    "Full-Time Contract Plan",
    "Part-Time Benefits",
    "Project-Based Compensation",
    "IT Department Package",
    "HR Excellence Plan",
    "Operations Basic Plan",
    "Growth Track Package",
    "Leadership Development Plan",
    "Sales Incentive Plan",
    "Research & Development Plan",
]

FIELDNAMES = [
    "employee_id", "employee_name", "employee_position",
    "plan_id", "plan_name", "plan_start_date",
    "compensation_id", "compensation_type", "currency", "effective_date",
    "annual_salary", "pay_frequency",
    "hourly_rate", "hours_worked",
    "bonus_amount", "trigger_criteria",
]

# ── generators ─────────────────────────────────────────────────────────────────


def _random_date(start_year: int = 2020, end_year: int = 2024) -> date:
    start = date(start_year, 1, 1)
    delta = (date(end_year, 12, 31) - start).days
    return start + timedelta(days=random.randint(0, delta))


def _generate_employees(count: int) -> list[dict]:
    employees: list[dict] = []
    used: set[str] = set()
    while len(employees) < count:
        full_name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
        if full_name in used:
            continue
        used.add(full_name)
        employees.append(
            {
                "employee_id": str(uuid.uuid4()),
                "employee_name": full_name,
                "employee_position": random.choice(POSITIONS),
            }
        )
    return employees


def _generate_plans(count: int) -> list[dict]:
    return [
        {
            "plan_id": str(uuid.uuid4()),
            "plan_name": PLAN_NAMES[i % len(PLAN_NAMES)],
            "plan_start_date": _random_date(2020, 2023).isoformat(),
        }
        for i in range(count)
    ]


def _generate_rows(
    employees: list[dict], plans: list[dict], total_rows: int
) -> list[dict]:
    rows: list[dict] = []
    base = total_rows // len(employees)
    extra = total_rows % len(employees)

    for idx, emp in enumerate(employees):
        count = base + (1 if idx < extra else 0)
        for _ in range(count):
            comp_type = random.choices(
                ["SALARY", "HOURLY", "BONUS"], weights=[40, 40, 20]
            )[0]
            plan = random.choice(plans)

            row: dict = {
                "employee_id": emp["employee_id"],
                "employee_name": emp["employee_name"],
                "employee_position": emp["employee_position"],
                "plan_id": plan["plan_id"],
                "plan_name": plan["plan_name"],
                "plan_start_date": plan["plan_start_date"],
                "compensation_id": str(uuid.uuid4()),
                "compensation_type": comp_type,
                "currency": random.choice(CURRENCIES),
                "effective_date": _random_date(2021, 2024).isoformat(),
                "annual_salary": "",
                "pay_frequency": "",
                "hourly_rate": "",
                "hours_worked": "",
                "bonus_amount": "",
                "trigger_criteria": "",
            }

            if comp_type == "SALARY":
                row["annual_salary"] = round(random.uniform(30_000, 200_000), 2)
                row["pay_frequency"] = random.choice(PAY_FREQUENCIES)
            elif comp_type == "HOURLY":
                row["hourly_rate"] = round(random.uniform(10, 150), 2)
                row["hours_worked"] = round(random.uniform(20, 60), 1)
            else:
                row["bonus_amount"] = round(random.uniform(500, 20_000), 2)
                row["trigger_criteria"] = random.choice(TRIGGER_CRITERIA)

            rows.append(row)

    return rows


# ── public API ─────────────────────────────────────────────────────────────────


def generate(
    output_path: str,
    num_employees: int = 50,
    num_plans: int = 20,
    num_rows: int = 1050,
) -> None:
    random.seed(42)
    employees = _generate_employees(num_employees)
    plans = _generate_plans(num_plans)
    rows = _generate_rows(employees, plans, num_rows)

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    with open(out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Generated {len(rows)} rows -> {out}")


# ── CLI ────────────────────────────────────────────────────────────────────────


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a compensation CSV data file with 1000+ rows."
    )
    parser.add_argument(
        "--output", default="data/compensations.csv", help="Output CSV path"
    )
    parser.add_argument(
        "--employees", type=int, default=50, help="Number of employees (default 50)"
    )
    parser.add_argument(
        "--plans", type=int, default=20, help="Number of compensation plans (default 20)"
    )
    parser.add_argument(
        "--rows", type=int, default=1050, help="Total data rows (min 1000)"
    )
    args = parser.parse_args()

    if args.rows < 1000:
        parser.error("--rows must be at least 1000")
    if args.employees < 1:
        parser.error("--employees must be at least 1")

    generate(args.output, args.employees, args.plans, args.rows)


if __name__ == "__main__":
    main()
