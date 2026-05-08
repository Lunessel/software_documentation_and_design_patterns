from sqlalchemy.orm import Session

from business_logic.models.compensation_plan import CompensationPlan
from data_access.interfaces.i_compensation_plan_repository import ICompensationPlanRepository
from data_access.orm.models import CompensationPlanORM


class CompensationPlanRepository(ICompensationPlanRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def save(self, plan: CompensationPlan) -> None:
        if not self.exists(plan.plan_id):
            self._session.add(self._to_orm(plan))
            self._session.commit()

    def save_all(self, plans: list[CompensationPlan]) -> None:
        for plan in plans:
            if not self.exists(plan.plan_id):
                self._session.add(self._to_orm(plan))
        self._session.commit()

    def get_by_id(self, plan_id: str) -> CompensationPlan | None:
        orm = self._session.get(CompensationPlanORM, plan_id)
        return self._to_domain(orm) if orm else None

    def get_all(self) -> list[CompensationPlan]:
        return [self._to_domain(o) for o in self._session.query(CompensationPlanORM).all()]

    def exists(self, plan_id: str) -> bool:
        return self._session.get(CompensationPlanORM, plan_id) is not None

    def _to_orm(self, plan: CompensationPlan) -> CompensationPlanORM:
        return CompensationPlanORM(
            plan_id=plan.plan_id,
            plan_name=plan.plan_name,
            start_date=plan.start_date,
        )

    def _to_domain(self, orm: CompensationPlanORM) -> CompensationPlan:
        return CompensationPlan(
            plan_id=orm.plan_id,
            plan_name=orm.plan_name,
            start_date=orm.start_date,
        )
