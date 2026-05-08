from __future__ import annotations
import uuid

from business_logic.models.employee import Employee
from data_access.interfaces.i_employee_repository import IEmployeeRepository


class EmployeeService:
    """BLL service — CRUD operations for Employee."""

    def __init__(self, repo: IEmployeeRepository) -> None:
        self._repo = repo

    def get_all(self) -> list[Employee]:
        return self._repo.get_all()

    def get_by_id(self, employee_id: str) -> Employee | None:
        return self._repo.get_by_id(employee_id)

    def create(self, name: str, position: str) -> Employee:
        emp = Employee(employee_id=str(uuid.uuid4()), name=name, position=position)
        self._repo.save(emp)
        return emp

    def update(self, employee_id: str, name: str, position: str) -> None:
        emp = Employee(employee_id=employee_id, name=name, position=position)
        self._repo.update(emp)

    def delete(self, employee_id: str) -> None:
        self._repo.delete(employee_id)
