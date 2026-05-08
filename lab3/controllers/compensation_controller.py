from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from typing import Annotated

import deps

router = APIRouter()
templates = Jinja2Templates(directory=str(Path(__file__).parent.parent / "templates"))

_CURRENCIES = ["UAH", "USD", "EUR"]
_PAY_FREQS = ["WEEKLY", "BIWEEKLY", "MONTHLY", "ANNUALLY"]
_COMP_TYPES = ["SALARY", "HOURLY", "BONUS"]


def _form_ctx(request: Request, compensation=None, employee_id: str = ""):
    comp_svc = deps.get_compensation_service()
    emp_svc = deps.get_employee_service()
    return {
        "request": request,
        "compensation": compensation,
        "employees": emp_svc.get_all(),
        "plans": comp_svc.get_all_plans(),
        "currencies": _CURRENCIES,
        "pay_frequencies": _PAY_FREQS,
        "comp_types": _COMP_TYPES,
        "preselect_employee": employee_id,
    }


@router.get("/compensations")
async def list_compensations(request: Request, employee_id: str = ""):
    comp_svc = deps.get_compensation_service()
    emp_svc = deps.get_employee_service()
    if employee_id:
        compensations = comp_svc.get_by_employee(employee_id)
    else:
        compensations = comp_svc.get_all()
    employees = emp_svc.get_all()
    emp_map = {e.employee_id: e.name for e in employees}
    return templates.TemplateResponse(
        "compensations/list.html",
        {
            "request": request,
            "compensations": compensations,
            "emp_map": emp_map,
            "employees": employees,
            "filter_employee": employee_id,
        },
    )


@router.get("/compensations/new")
async def new_compensation_form(request: Request, employee_id: str = ""):
    return templates.TemplateResponse(
        "compensations/form.html",
        {**_form_ctx(request, employee_id=employee_id), "title": "New Compensation"},
    )


@router.post("/compensations")
async def create_compensation(
    request: Request,
    compensation_type: Annotated[str, Form()],
    currency: Annotated[str, Form()],
    effective_date: Annotated[str, Form()],
    employee_id: Annotated[str, Form()],
    plan_id: Annotated[str, Form()] = "",
    annual_salary: Annotated[str, Form()] = "",
    pay_frequency: Annotated[str, Form()] = "",
    hourly_rate: Annotated[str, Form()] = "",
    hours_worked: Annotated[str, Form()] = "",
    bonus_amount: Annotated[str, Form()] = "",
    trigger_criteria: Annotated[str, Form()] = "",
):
    form = {
        "compensation_type": compensation_type,
        "currency": currency,
        "effective_date": effective_date,
        "employee_id": employee_id,
        "plan_id": plan_id,
        "annual_salary": annual_salary,
        "pay_frequency": pay_frequency,
        "hourly_rate": hourly_rate,
        "hours_worked": hours_worked,
        "bonus_amount": bonus_amount,
        "trigger_criteria": trigger_criteria,
    }
    deps.get_compensation_service().create(form)
    return RedirectResponse(url=f"/employees/{employee_id}", status_code=303)


@router.get("/compensations/{comp_id}/edit")
async def edit_compensation_form(request: Request, comp_id: str):
    comp = deps.get_compensation_service().get_by_id(comp_id)
    if not comp:
        return RedirectResponse(url="/compensations", status_code=302)
    return templates.TemplateResponse(
        "compensations/form.html",
        {**_form_ctx(request, compensation=comp), "title": "Edit Compensation"},
    )


@router.post("/compensations/{comp_id}/edit")
async def update_compensation(
    comp_id: str,
    compensation_type: Annotated[str, Form()],
    currency: Annotated[str, Form()],
    effective_date: Annotated[str, Form()],
    employee_id: Annotated[str, Form()],
    plan_id: Annotated[str, Form()] = "",
    annual_salary: Annotated[str, Form()] = "",
    pay_frequency: Annotated[str, Form()] = "",
    hourly_rate: Annotated[str, Form()] = "",
    hours_worked: Annotated[str, Form()] = "",
    bonus_amount: Annotated[str, Form()] = "",
    trigger_criteria: Annotated[str, Form()] = "",
):
    form = {
        "compensation_type": compensation_type,
        "currency": currency,
        "effective_date": effective_date,
        "employee_id": employee_id,
        "plan_id": plan_id,
        "annual_salary": annual_salary,
        "pay_frequency": pay_frequency,
        "hourly_rate": hourly_rate,
        "hours_worked": hours_worked,
        "bonus_amount": bonus_amount,
        "trigger_criteria": trigger_criteria,
    }
    deps.get_compensation_service().update(comp_id, form)
    return RedirectResponse(url=f"/employees/{employee_id}", status_code=303)


@router.post("/compensations/{comp_id}/delete")
async def delete_compensation(comp_id: str, employee_id: str = Form("")):
    deps.get_compensation_service().delete(comp_id)
    if employee_id:
        return RedirectResponse(url=f"/employees/{employee_id}", status_code=303)
    return RedirectResponse(url="/compensations", status_code=303)
