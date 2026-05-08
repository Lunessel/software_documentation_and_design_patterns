from __future__ import annotations
import uuid
from datetime import datetime

from business_logic.models.bonus_compensation import BonusCompensation
from business_logic.models.compensation import Compensation
from business_logic.models.compensation_plan import CompensationPlan
from business_logic.models.hourly_compensation import HourlyCompensation
from business_logic.models.salary_compensation import PayFrequency, SalaryCompensation
from data_access.interfaces.i_compensation_plan_repository import ICompensationPlanRepository
from data_access.interfaces.i_compensation_repository import ICompensationRepository

_DATE_FMT = "%Y-%m-%d"


class CompensationService:
    """BLL service — CRUD operations for Compensation."""

    def __init__(
        self,
        comp_repo: ICompensationRepository,
        plan_repo: ICompensationPlanRepository,
    ) -> None:
        self._comp_repo = comp_repo
        self._plan_repo = plan_repo

    def get_all(self) -> list[Compensation]:
        return self._comp_repo.get_all()

    def get_by_id(self, compensation_id: str) -> Compensation | None:
        return self._comp_repo.get_by_id(compensation_id)

    def get_by_employee(self, employee_id: str) -> list[Compensation]:
        return self._comp_repo.get_by_employee_id(employee_id)

    def get_all_plans(self) -> list[CompensationPlan]:
        return self._plan_repo.get_all()

    def create(self, form: dict) -> Compensation:
        comp = self._build(str(uuid.uuid4()), form)
        self._comp_repo.save(comp)
        return comp

    def update(self, compensation_id: str, form: dict) -> None:
        comp = self._build(compensation_id, form)
        self._comp_repo.update(comp)

    def delete(self, compensation_id: str) -> None:
        self._comp_repo.delete(compensation_id)

    def _build(self, comp_id: str, form: dict) -> Compensation:
        comp_type = form["compensation_type"]
        currency = form["currency"]
        effective_date = datetime.strptime(form["effective_date"], _DATE_FMT).date()
        employee_id = form["employee_id"]
        plan_id = form.get("plan_id") or None

        if comp_type == "SALARY":
            return SalaryCompensation(
                compensation_id=comp_id,
                currency=currency,
                effective_date=effective_date,
                employee_id=employee_id,
                annual_salary=float(form["annual_salary"]),
                pay_frequency=PayFrequency[form["pay_frequency"]],
                plan_id=plan_id,
            )
        if comp_type == "HOURLY":
            return HourlyCompensation(
                compensation_id=comp_id,
                currency=currency,
                effective_date=effective_date,
                employee_id=employee_id,
                hourly_rate=float(form["hourly_rate"]),
                hours_worked=float(form["hours_worked"]),
                plan_id=plan_id,
            )
        return BonusCompensation(
            compensation_id=comp_id,
            currency=currency,
            effective_date=effective_date,
            employee_id=employee_id,
            bonus_amount=float(form["bonus_amount"]),
            trigger_criteria=form["trigger_criteria"],
            plan_id=plan_id,
        )
