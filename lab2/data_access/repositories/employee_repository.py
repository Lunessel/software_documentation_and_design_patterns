from sqlalchemy.orm import Session

from business_logic.models.employee import Employee
from data_access.interfaces.i_employee_repository import IEmployeeRepository
from data_access.orm.models import EmployeeORM


class EmployeeRepository(IEmployeeRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def save(self, employee: Employee) -> None:
        if not self.exists(employee.employee_id):
            self._session.add(self._to_orm(employee))
            self._session.commit()

    def save_all(self, employees: list[Employee]) -> None:
        for emp in employees:
            if not self.exists(emp.employee_id):
                self._session.add(self._to_orm(emp))
        self._session.commit()

    def get_by_id(self, employee_id: str) -> Employee | None:
        orm = self._session.get(EmployeeORM, employee_id)
        return self._to_domain(orm) if orm else None

    def get_all(self) -> list[Employee]:
        return [self._to_domain(o) for o in self._session.query(EmployeeORM).all()]

    def exists(self, employee_id: str) -> bool:
        return self._session.get(EmployeeORM, employee_id) is not None

    def update(self, employee: Employee) -> None:
        orm = self._session.get(EmployeeORM, employee.employee_id)
        if orm:
            orm.name = employee.name
            orm.position = employee.position
            self._session.commit()

    def delete(self, employee_id: str) -> None:
        orm = self._session.get(EmployeeORM, employee_id)
        if orm:
            self._session.delete(orm)
            self._session.commit()

    def _to_orm(self, emp: Employee) -> EmployeeORM:
        return EmployeeORM(
            employee_id=emp.employee_id,
            name=emp.name,
            position=emp.position,
        )

    def _to_domain(self, orm: EmployeeORM) -> Employee:
        return Employee(
            employee_id=orm.employee_id,
            name=orm.name,
            position=orm.position,
        )
