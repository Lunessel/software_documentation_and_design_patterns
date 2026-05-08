from sqlalchemy.orm import Session

from business_logic.models.bonus_compensation import BonusCompensation
from business_logic.models.compensation import Compensation
from business_logic.models.hourly_compensation import HourlyCompensation
from business_logic.models.salary_compensation import PayFrequency, SalaryCompensation
from data_access.interfaces.i_compensation_repository import ICompensationRepository
from data_access.orm.models import CompensationORM


class CompensationRepository(ICompensationRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def save(self, compensation: Compensation) -> None:
        self._session.add(self._to_orm(compensation))
        self._session.commit()

    def save_all(self, compensations: list[Compensation]) -> None:
        for comp in compensations:
            if self._session.get(CompensationORM, comp.compensation_id) is None:
                self._session.add(self._to_orm(comp))
        self._session.commit()

    def get_all(self) -> list[Compensation]:
        return [self._to_domain(o) for o in self._session.query(CompensationORM).all()]

    def get_by_id(self, compensation_id: str) -> Compensation | None:
        orm = self._session.get(CompensationORM, compensation_id)
        return self._to_domain(orm) if orm else None

    def get_by_employee_id(self, employee_id: str) -> list[Compensation]:
        orms = self._session.query(CompensationORM).filter_by(employee_id=employee_id).all()
        return [self._to_domain(o) for o in orms]

    def update(self, compensation: Compensation) -> None:
        orm = self._session.get(CompensationORM, compensation.compensation_id)
        if not orm:
            return
        orm.currency = compensation.currency
        orm.effective_date = compensation.effective_date
        orm.employee_id = compensation.employee_id
        orm.plan_id = compensation.plan_id
        orm.annual_salary = orm.pay_frequency = None
        orm.hourly_rate = orm.hours_worked = None
        orm.bonus_amount = orm.trigger_criteria = None
        if isinstance(compensation, SalaryCompensation):
            orm.compensation_type = "SALARY"
            orm.annual_salary = compensation.annual_salary
            orm.pay_frequency = compensation.pay_frequency.value
        elif isinstance(compensation, HourlyCompensation):
            orm.compensation_type = "HOURLY"
            orm.hourly_rate = compensation.hourly_rate
            orm.hours_worked = compensation.hours_worked
        elif isinstance(compensation, BonusCompensation):
            orm.compensation_type = "BONUS"
            orm.bonus_amount = compensation.bonus_amount
            orm.trigger_criteria = compensation.trigger_criteria
        self._session.commit()

    def delete(self, compensation_id: str) -> None:
        orm = self._session.get(CompensationORM, compensation_id)
        if orm:
            self._session.delete(orm)
            self._session.commit()

    def _to_orm(self, comp: Compensation) -> CompensationORM:
        orm = CompensationORM(
            compensation_id=comp.compensation_id,
            currency=comp.currency,
            effective_date=comp.effective_date,
            employee_id=comp.employee_id,
            plan_id=comp.plan_id,
        )
        if isinstance(comp, SalaryCompensation):
            orm.compensation_type = "SALARY"
            orm.annual_salary = comp.annual_salary
            orm.pay_frequency = comp.pay_frequency.value
        elif isinstance(comp, HourlyCompensation):
            orm.compensation_type = "HOURLY"
            orm.hourly_rate = comp.hourly_rate
            orm.hours_worked = comp.hours_worked
        elif isinstance(comp, BonusCompensation):
            orm.compensation_type = "BONUS"
            orm.bonus_amount = comp.bonus_amount
            orm.trigger_criteria = comp.trigger_criteria
        return orm

    def _to_domain(self, orm: CompensationORM) -> Compensation:
        if orm.compensation_type == "SALARY":
            return SalaryCompensation(
                compensation_id=orm.compensation_id,
                currency=orm.currency,
                effective_date=orm.effective_date,
                employee_id=orm.employee_id,
                annual_salary=orm.annual_salary,
                pay_frequency=PayFrequency[orm.pay_frequency],
                plan_id=orm.plan_id,
            )
        if orm.compensation_type == "HOURLY":
            return HourlyCompensation(
                compensation_id=orm.compensation_id,
                currency=orm.currency,
                effective_date=orm.effective_date,
                employee_id=orm.employee_id,
                hourly_rate=orm.hourly_rate,
                hours_worked=orm.hours_worked,
                plan_id=orm.plan_id,
            )
        return BonusCompensation(
            compensation_id=orm.compensation_id,
            currency=orm.currency,
            effective_date=orm.effective_date,
            employee_id=orm.employee_id,
            bonus_amount=orm.bonus_amount,
            trigger_criteria=orm.trigger_criteria,
            plan_id=orm.plan_id,
        )
