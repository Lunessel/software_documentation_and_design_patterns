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
