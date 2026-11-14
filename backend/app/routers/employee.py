""" Crud APIs"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database.connection import get_db
from app.models.employee import Employee
from app.schemas.employee import (
    EmployeeCreate,
    EmployeeResponse,
    EmployeeUpdate
)

router = APIRouter(
    prefix="/api/employees",
    tags=["Employees"]
)


# create employee
@router.post("/", response_model=EmployeeResponse, status_code=201)
def create_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db)
):
    existing = db.query(Employee).filter(
        Employee.email == employee.email
    ).first()

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Employee email already exists"
        )

    new_employee = Employee(**employee.model_dump())

    try:
        db.add(new_employee)
        db.commit()
        db.refresh(new_employee)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Employee email already exists"
        )

    return new_employee


# get all employee
@router.get("/", response_model=list[EmployeeResponse])
def get_employees(db: Session = Depends(get_db)):
    return db.query(Employee).order_by(Employee.id).all()


@router.get("/search", response_model=list[EmployeeResponse])
def search_employees(
    name: str,
    db: Session = Depends(get_db)
):
    employees = db.query(Employee).filter(
        Employee.name.ilike(f"%{name}%")
    ).all()

    return employees



@router.get("/filter", response_model=list[EmployeeResponse])
def filter_employees(
    department: str | None = None,
    designation: str | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(Employee)

    if department:
        query = query.filter(
            Employee.department == department
        )

    if designation:
        query = query.filter(
            Employee.designation == designation
        )

    return query.all()

@router.get("/filter-salary", response_model=list[EmployeeResponse])
def filter_by_salary(
    min_salary: float,
    max_salary: float,
    db: Session = Depends(get_db)
):
    if min_salary > max_salary:
        raise HTTPException(
            status_code=400,
            detail="Minimum salary cannot exceed maximum salary"
        )

    return db.query(Employee).filter(
        Employee.salary.between(min_salary, max_salary)
    ).all()

@router.get("/pagination")
def get_employees_paginated(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    total = db.query(Employee).count()

    employees = (
        db.query(Employee)
        .offset(skip)
        .limit(limit)
        .all()
    )

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "employees": employees
    }

@router.put("/{employee_id}", response_model=EmployeeResponse)
def update_employee(
    employee_id: int,
    employee: EmployeeCreate,
    db: Session = Depends(get_db)
):
    existing_employee = db.query(Employee).filter(
        Employee.id == employee_id
    ).first()

    if not existing_employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    duplicate_email = db.query(Employee).filter(
        Employee.email == employee.email,
        Employee.id != employee_id
    ).first()

    if duplicate_email:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    for key, value in employee.model_dump().items():
        setattr(existing_employee, key, value)

    db.commit()
    db.refresh(existing_employee)

    return existing_employee

# get employee by id
@router.get("/{employee_id}", response_model=EmployeeResponse)
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):
    employee = db.query(Employee).filter(
        Employee.id == employee_id
    ).first()

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return employee


# update employee
@router.patch("/{employee_id}", response_model=EmployeeResponse)
def update_employee(
    employee_id: int,
    employee_data: EmployeeUpdate,
    db: Session = Depends(get_db)
):
    employee = db.query(Employee).filter(
        Employee.id == employee_id
    ).first()

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    update_data = employee_data.model_dump(exclude_unset=True)

    if "email" in update_data:
        existing = db.query(Employee).filter(
            Employee.email == update_data["email"],
            Employee.id != employee_id
        ).first()

        if existing:
            raise HTTPException(
                status_code=409,
                detail="Email already belongs to another employee"
            )

    for key, value in update_data.items():
        setattr(employee, key, value)

    try:
        db.commit()
        db.refresh(employee)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Employee update conflicts with existing data"
        )

    return employee


# delete employee
@router.delete("/{employee_id}")
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):
    employee = db.query(Employee).filter(
        Employee.id == employee_id
    ).first()

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    db.delete(employee)
    db.commit()

    return {"message": "Employee deleted successfully"}

