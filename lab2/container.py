from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from business_logic.services.compensation_service import CompensationImportService
from data_access.orm.models import Base
from data_access.repositories.compensation_plan_repository import CompensationPlanRepository
from data_access.repositories.compensation_repository import CompensationRepository
from data_access.repositories.csv_reader import CSVReader
from data_access.repositories.employee_repository import EmployeeRepository


class Container:
    """IoC container — wires DAL implementations into BLL via interfaces."""

    def __init__(self, db_url: str = "sqlite:///data/compensation.db") -> None:
        engine = create_engine(db_url, echo=False)
        Base.metadata.create_all(engine)

        session: Session = sessionmaker(bind=engine)()

        # DAL — concrete implementations
        csv_reader = CSVReader()
        employee_repo = EmployeeRepository(session)
        compensation_repo = CompensationRepository(session)
        plan_repo = CompensationPlanRepository(session)

        # BLL — receives only DAL interfaces, not implementations
        self._import_service = CompensationImportService(
            csv_reader=csv_reader,
            employee_repo=employee_repo,
            compensation_repo=compensation_repo,
            plan_repo=plan_repo,
        )

        self._session = session

    @property
    def import_service(self) -> CompensationImportService:
        return self._import_service

    def close(self) -> None:
        self._session.close()
