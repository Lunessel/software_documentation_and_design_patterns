from __future__ import annotations
from datetime import date

from business_logic.models.compensation import Compensation


class BonusCompensation(Compensation):
    def __init__(
        self,
        compensation_id: str,
        currency: str,
        effective_date: date,
        employee_id: str,
        bonus_amount: float,
        trigger_criteria: str,
        plan_id: str | None = None,
    ) -> None:
        super().__init__(compensation_id, currency, effective_date, employee_id, plan_id)
        self.bonus_amount = bonus_amount
        self.trigger_criteria = trigger_criteria

    def calculate(self) -> float:
        return self.bonus_amount if self.is_eligible() else 0.0

    def is_eligible(self) -> bool:
        return bool(self.trigger_criteria) and self.bonus_amount > 0

    def get_annual_bonus(self) -> float:
        return self.bonus_amount
