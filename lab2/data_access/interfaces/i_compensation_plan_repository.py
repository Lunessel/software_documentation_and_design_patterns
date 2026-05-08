from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from business_logic.models.compensation_plan import CompensationPlan


class ICompensationPlanRepository(ABC):
    @abstractmethod
    def save(self, plan: CompensationPlan) -> None: ...

    @abstractmethod
    def save_all(self, plans: list[CompensationPlan]) -> None: ...

    @abstractmethod
    def get_by_id(self, plan_id: str) -> CompensationPlan | None: ...

    @abstractmethod
    def get_all(self) -> list[CompensationPlan]: ...

    @abstractmethod
    def exists(self, plan_id: str) -> bool: ...
