from __future__ import annotations
from datetime import date
from enum import Enum

from business_logic.models.compensation import Compensation


class PayFrequency(Enum):
    WEEKLY = "WEEKLY"
    BIWEEKLY = "BIWEEKLY"
    MONTHLY = "MONTHLY"
    ANNUALLY = "ANNUALLY"


class SalaryCompensation(Compensation):
    def __init__(
        self,
        compensation_id: str,
        currency: str,
        effective_date: date,
        employee_id: str,
        annual_salary: float,
        pay_frequency: PayFrequency,
        plan_id: str | None = None,
    ) -> None:
        super().__init__(compensation_id, currency, effective_date, employee_id, plan_id)
        self.annual_salary = annual_salary
        self.pay_frequency = pay_frequency

    def calculate(self) -> float:
        return self.annual_salary

    def apply_raise(self, percentage: float) -> None:
        self.annual_salary *= 1 + percentage / 100

    def get_monthly_amount(self) -> float:
        return self.annual_salary / 12
