from __future__ import annotations


class Employee:
    def __init__(self, employee_id: str, name: str, position: str) -> None:
        self.employee_id = employee_id
        self.name = name
        self.position = position

    def get_compensations(self) -> list:
        return []

    def get_active_plan(self):
        return None

    def __repr__(self) -> str:
        return f"Employee(id={self.employee_id}, name={self.name}, position={self.position})"
