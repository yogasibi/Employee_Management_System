"""Provides a database session to API requests"""
from pydantic import BaseModel, EmailStr, ConfigDict

class EmployeeCreate(BaseModel):
    name: str
    email: EmailStr
    department: str
    designation: str
    salary: float


class EmployeeResponse(BaseModel):
    id: int
    name:str
    email: EmailStr
    department: str
    designation: str
    salary: float
    is_active: bool

    model_config = ConfigDict(from_attributes=True)

class EmployeeUpdate(BaseModel):
    name:str | None= None
    email: EmailStr | None = None
    department:str | None= None
    designation:str | None= None
    is_active:bool | None= None
    salary:float | None= None