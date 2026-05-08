from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from business_logic.models.compensation import Compensation


class ICompensationRepository(ABC):
    @abstractmethod
    def save(self, compensation: Compensation) -> None: ...

    @abstractmethod
    def save_all(self, compensations: list[Compensation]) -> None: ...

    @abstractmethod
    def get_all(self) -> list[Compensation]: ...

    @abstractmethod
    def get_by_id(self, compensation_id: str) -> Compensation | None: ...

    @abstractmethod
    def get_by_employee_id(self, employee_id: str) -> list[Compensation]: ...

    @abstractmethod
    def update(self, compensation: Compensation) -> None: ...

    @abstractmethod
    def delete(self, compensation_id: str) -> None: ...
