from sqlalchemy import Column, String, Float, Date, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class EmployeeORM(Base):
    __tablename__ = "employees"

    employee_id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    position = Column(String, nullable=False)

    compensations = relationship("CompensationORM", back_populates="employee")


class CompensationPlanORM(Base):
    __tablename__ = "compensation_plans"

    plan_id = Column(String, primary_key=True)
    plan_name = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)

    compensations = relationship("CompensationORM", back_populates="plan")


class CompensationORM(Base):
    __tablename__ = "compensations"

    compensation_id = Column(String, primary_key=True)
    compensation_type = Column(String, nullable=False)
    currency = Column(String, nullable=False)
    effective_date = Column(Date, nullable=False)

    employee_id = Column(String, ForeignKey("employees.employee_id"), nullable=False)
    plan_id = Column(String, ForeignKey("compensation_plans.plan_id"), nullable=True)

    # SalaryCompensation
    annual_salary = Column(Float, nullable=True)
    pay_frequency = Column(String, nullable=True)

    # HourlyCompensation
    hourly_rate = Column(Float, nullable=True)
    hours_worked = Column(Float, nullable=True)

    # BonusCompensation
    bonus_amount = Column(Float, nullable=True)
    trigger_criteria = Column(String, nullable=True)

    employee = relationship("EmployeeORM", back_populates="compensations")
    plan = relationship("CompensationPlanORM", back_populates="compensations")
