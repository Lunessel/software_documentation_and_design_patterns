from __future__ import annotations
from container import Container

_container: Container | None = None


def init(db_url: str | None = None) -> None:
    global _container
    _container = Container(db_url)


def get_employee_service():
    return _container.employee_service


def get_compensation_service():
    return _container.compensation_service
