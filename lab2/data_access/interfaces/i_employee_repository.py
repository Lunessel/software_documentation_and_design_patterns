from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from business_logic.models.employee import Employee


class IEmployeeRepository(ABC):
    @abstractmethod
    def save(self, employee: Employee) -> None: ...

    @abstractmethod
    def save_all(self, employees: list[Employee]) -> None: ...

    @abstractmethod
    def get_by_id(self, employee_id: str) -> Employee | None: ...

    @abstractmethod
    def get_all(self) -> list[Employee]: ...

    @abstractmethod
    def exists(self, employee_id: str) -> bool: ...

    @abstractmethod
    def update(self, employee: Employee) -> None: ...

    @abstractmethod
    def delete(self, employee_id: str) -> None: ...
