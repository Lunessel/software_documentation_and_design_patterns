import sys
from pathlib import Path

# Make lab2 packages (data_access, business_logic) available
sys.path.append(str(Path(__file__).parent.parent / "lab2"))

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from data_access.orm.models import Base
from data_access.repositories.compensation_plan_repository import CompensationPlanRepository
from data_access.repositories.compensation_repository import CompensationRepository
from data_access.repositories.employee_repository import EmployeeRepository
from services.employee_service import EmployeeService
from services.compensation_service import CompensationService

_LAB2_DB = Path(__file__).parent.parent / "lab2" / "data" / "compensation.db"


class Container:
    """IoC container — wires lab2 DAL implementations into lab3 BLL services."""

    def __init__(self, db_url: str | None = None) -> None:
        url = db_url or f"sqlite:///{_LAB2_DB}"
        engine = create_engine(url, echo=False)
        Base.metadata.create_all(engine)

        session: Session = sessionmaker(bind=engine)()

        employee_repo = EmployeeRepository(session)
        compensation_repo = CompensationRepository(session)
        plan_repo = CompensationPlanRepository(session)

        self.employee_service = EmployeeService(employee_repo)
        self.compensation_service = CompensationService(compensation_repo, plan_repo)

        self._session = session

    def close(self) -> None:
        self._session.close()
