""" main entry point """

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.connection import Base, engine
from app.models.employee import Employee
from app.routers import employee

app = FastAPI(
    title="Employee Management System",
    description="Employee and Project Management APIs",
    version="1.0.0"
)


Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(employee.router)


@app.get("/")
def home():
    return {
        "message": "Employee Management API is running"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}
