"""
Lab 3 — MVC web app with FastAPI + Jinja2.

Run:
    uvicorn main:app --reload

Prerequisites:
    pip install -r requirements.txt
    cd ../lab2 && python generate_csv.py && python main.py  # seed the DB
"""

import sys
from pathlib import Path

# Ensure lab2 packages are importable
sys.path.append(str(Path(__file__).parent.parent / "lab2"))

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import deps
from controllers.employee_controller import router as employee_router
from controllers.compensation_controller import router as compensation_router

deps.init()

app = FastAPI(title="Compensation Manager")
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(employee_router)
app.include_router(compensation_router)

templates = Jinja2Templates(directory="templates")


@app.get("/")
async def index(request: Request):
    emp_svc = deps.get_employee_service()
    comp_svc = deps.get_compensation_service()
    employees = emp_svc.get_all()
    compensations = comp_svc.get_all()
    total_cost = sum(c.calculate() for c in compensations)
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "employee_count": len(employees),
            "compensation_count": len(compensations),
            "total_cost": total_cost,
            "recent_employees": employees[:5],
        },
    )


@app.get("/favicon.ico")
async def favicon():
    return RedirectResponse(url="/static/favicon.ico", status_code=302)
