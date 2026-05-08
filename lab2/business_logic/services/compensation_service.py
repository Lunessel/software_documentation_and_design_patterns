from __future__ import annotations

from datetime import datetime

from business_logic.models.bonus_compensation import BonusCompensation
from business_logic.models.compensation import Compensation
from business_logic.models.compensation_plan import CompensationPlan
from business_logic.models.employee import Employee
from business_logic.models.hourly_compensation import HourlyCompensation
from business_logic.models.salary_compensation import PayFrequency, SalaryCompensation
from data_access.interfaces.i_compensation_plan_repository import ICompensationPlanRepository
from data_access.interfaces.i_compensation_repository import ICompensationRepository
from data_access.interfaces.i_csv_reader import ICSVReader
from data_access.interfaces.i_employee_repository import IEmployeeRepository

_DATE_FMT = "%Y-%m-%d"


class CompensationImportService:
    """BLL service — orchestrates CSV import into DB via DAL interfaces."""

    def __init__(
        self,
        csv_reader: ICSVReader,
        employee_repo: IEmployeeRepository,
        compensation_repo: ICompensationRepository,
        plan_repo: ICompensationPlanRepository,
    ) -> None:
        self._csv_reader = csv_reader
        self._employee_repo = employee_repo
        self._compensation_repo = compensation_repo
        self._plan_repo = plan_repo

    def import_from_csv(self, file_path: str) -> None:
        rows = self._csv_reader.read(file_path)

        employees: dict[str, Employee] = {}
        plans: dict[str, CompensationPlan] = {}
        compensations: list[Compensation] = []

        for row in rows:
            emp_id = row["employee_id"]
            if emp_id not in employees:
                employees[emp_id] = Employee(
                    employee_id=emp_id,
                    name=row["employee_name"],
                    position=row["employee_position"],
                )

            plan_id = row.get("plan_id", "").strip()
            if plan_id and plan_id not in plans:
                plans[plan_id] = CompensationPlan(
                    plan_id=plan_id,
                    plan_name=row["plan_name"],
                    start_date=datetime.strptime(row["plan_start_date"], _DATE_FMT).date(),
                )

            comp = self._build_compensation(row, emp_id, plan_id or None)
            if comp is not None:
                compensations.append(comp)

        self._employee_repo.save_all(list(employees.values()))
        self._plan_repo.save_all(list(plans.values()))
        self._compensation_repo.save_all(compensations)

        print(
            f"Imported: {len(employees)} employees, "
            f"{len(plans)} plans, "
            f"{len(compensations)} compensations."
        )

    def _build_compensation(
        self, row: dict, emp_id: str, plan_id: str | None
    ) -> Compensation | None:
        comp_type = row.get("compensation_type", "").strip()
        comp_id = row["compensation_id"]
        currency = row["currency"]
        effective_date = datetime.strptime(row["effective_date"], _DATE_FMT).date()

        if comp_type == "SALARY":
            return SalaryCompensation(
                compensation_id=comp_id,
                currency=currency,
                effective_date=effective_date,
                employee_id=emp_id,
                annual_salary=float(row["annual_salary"]),
                pay_frequency=PayFrequency[row["pay_frequency"]],
                plan_id=plan_id,
            )
        if comp_type == "HOURLY":
            return HourlyCompensation(
                compensation_id=comp_id,
                currency=currency,
                effective_date=effective_date,
                employee_id=emp_id,
                hourly_rate=float(row["hourly_rate"]),
                hours_worked=float(row["hours_worked"]),
                plan_id=plan_id,
            )
        if comp_type == "BONUS":
            return BonusCompensation(
                compensation_id=comp_id,
                currency=currency,
                effective_date=effective_date,
                employee_id=emp_id,
                bonus_amount=float(row["bonus_amount"]),
                trigger_criteria=row["trigger_criteria"],
                plan_id=plan_id,
            )
        return None
