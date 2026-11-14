from sqlalchemy import (
    Column, Integer, String, Text, Date,
    DateTime
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database.connection import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(150), nullable=False)
    description = Column(Text)

    status = Column(String(50), default="Planning")

    start_date = Column(Date)
    end_date = Column(Date)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # Many-to-many relationship
    employees = relationship(
        "Employee",
        secondary="project_members",
        back_populates="projects"
    )

    # One-to-many relationship
    tasks = relationship(
        "Task",
        back_populates="project",
        cascade="all, delete-orphan"
    )