from abc import ABC, abstractmethod


class ICompensationController(ABC):
    @abstractmethod
    def get_all_compensations(self) -> list: ...

    @abstractmethod
    def get_compensations_by_employee(self, employee_id: str) -> list: ...

    @abstractmethod
    def import_from_csv(self, file_path: str) -> None: ...
