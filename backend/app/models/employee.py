"""Creates database sessions"""
from sqlalchemy.orm import sessionmaker
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    func,
    Float,
)
from sqlalchemy.orm import relationship

from app.database.connection import Base


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    department = Column(String(100), nullable=False)
    designation = Column(String(100), nullable=False)
    salary = Column(Float(100), nullable=False)
    is_active = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Many-to-many relationship
    projects = relationship(
        "Project",
        secondary="project_members",
        back_populates="employees"
    )

    # One-to-many relationship
    tasks = relationship(
        "Task",
        back_populates="employee"
    )