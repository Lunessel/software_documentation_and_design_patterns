from abc import ABC, abstractmethod


class IEmployeeController(ABC):
    @abstractmethod
    def get_all_employees(self) -> list: ...

    @abstractmethod
    def get_employee_by_id(self, employee_id: str): ...
