from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import date


class Compensation(ABC):
    def __init__(
        self,
        compensation_id: str,
        currency: str,
        effective_date: date,
        employee_id: str,
        plan_id: str | None = None,
    ) -> None:
        self.compensation_id = compensation_id
        self.currency = currency
        self.effective_date = effective_date
        self.employee_id = employee_id
        self.plan_id = plan_id

    @abstractmethod
    def calculate(self) -> float: ...

    def get_summary(self) -> str:
        return (
            f"Compensation {self.compensation_id} | {self.currency} | "
            f"effective {self.effective_date} | amount={self.calculate():.2f}"
        )

    def validate(self) -> bool:
        return bool(
            self.compensation_id
            and self.currency
            and self.effective_date
            and self.employee_id
        )
