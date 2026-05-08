from __future__ import annotations
from datetime import date

from business_logic.models.compensation import Compensation


class CompensationPlan:
    def __init__(self, plan_id: str, plan_name: str, start_date: date) -> None:
        self.plan_id = plan_id
        self.plan_name = plan_name
        self.start_date = start_date
        self.items: list[Compensation] = []

    def add_item(self, compensation: Compensation) -> None:
        self.items.append(compensation)

    def get_total_cost(self) -> float:
        return sum(c.calculate() for c in self.items)

    def __repr__(self) -> str:
        return f"CompensationPlan(id={self.plan_id}, name={self.plan_name})"
