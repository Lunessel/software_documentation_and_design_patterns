from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

import deps

router = APIRouter()
templates = Jinja2Templates(directory=str(Path(__file__).parent.parent / "templates"))


@router.get("/employees")
async def list_employees(request: Request):
    emp_svc = deps.get_employee_service()
    comp_svc = deps.get_compensation_service()
    employees = emp_svc.get_all()
    rows = [
        {"employee": e, "comp_count": len(comp_svc.get_by_employee(e.employee_id))}
        for e in employees
    ]
    return templates.TemplateResponse(
        "employees/list.html", {"request": request, "rows": rows}
    )


@router.get("/employees/new")
async def new_employee_form(request: Request):
    return templates.TemplateResponse(
        "employees/form.html",
        {"request": request, "employee": None, "title": "New Employee"},
    )


@router.post("/employees")
async def create_employee(
    name: str = Form(...),
    position: str = Form(...),
):
    deps.get_employee_service().create(name=name, position=position)
    return RedirectResponse(url="/employees", status_code=303)


@router.get("/employees/{employee_id}")
async def detail_employee(request: Request, employee_id: str):
    emp_svc = deps.get_employee_service()
    employee = emp_svc.get_by_id(employee_id)
    if not employee:
        return RedirectResponse(url="/employees", status_code=302)
    compensations = deps.get_compensation_service().get_by_employee(employee_id)
    return templates.TemplateResponse(
        "employees/detail.html",
        {"request": request, "employee": employee, "compensations": compensations},
    )


@router.get("/employees/{employee_id}/edit")
async def edit_employee_form(request: Request, employee_id: str):
    employee = deps.get_employee_service().get_by_id(employee_id)
    if not employee:
        return RedirectResponse(url="/employees", status_code=302)
    return templates.TemplateResponse(
        "employees/form.html",
        {"request": request, "employee": employee, "title": "Edit Employee"},
    )


@router.post("/employees/{employee_id}/edit")
async def update_employee(
    employee_id: str,
    name: str = Form(...),
    position: str = Form(...),
):
    deps.get_employee_service().update(employee_id, name=name, position=position)
    return RedirectResponse(url=f"/employees/{employee_id}", status_code=303)


@router.post("/employees/{employee_id}/delete")
async def delete_employee(employee_id: str):
    deps.get_employee_service().delete(employee_id)
    return RedirectResponse(url="/employees", status_code=303)
