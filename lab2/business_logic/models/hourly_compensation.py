from __future__ import annotations
from datetime import date

from business_logic.models.compensation import Compensation

_OVERTIME_THRESHOLD = 40.0
_OVERTIME_MULTIPLIER = 1.5


class HourlyCompensation(Compensation):
    def __init__(
        self,
        compensation_id: str,
        currency: str,
        effective_date: date,
        employee_id: str,
        hourly_rate: float,
        hours_worked: float,
        plan_id: str | None = None,
    ) -> None:
        super().__init__(compensation_id, currency, effective_date, employee_id, plan_id)
        self.hourly_rate = hourly_rate
        self.hours_worked = hours_worked

    def calculate(self) -> float:
        regular = min(self.hours_worked, _OVERTIME_THRESHOLD)
        overtime = max(0.0, self.hours_worked - _OVERTIME_THRESHOLD)
        return regular * self.hourly_rate + overtime * self.hourly_rate * _OVERTIME_MULTIPLIER

    def calc_overtime(self) -> float:
        overtime = max(0.0, self.hours_worked - _OVERTIME_THRESHOLD)
        return overtime * self.hourly_rate * _OVERTIME_MULTIPLIER

    def get_weekly_amount(self) -> float:
        return self.calculate()
