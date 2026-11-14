from sqlalchemy import (
    Column, Integer, String, Text, Date,
    DateTime, ForeignKey
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database.connection import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(150), nullable=False)
    description = Column(Text)

    status = Column(String(50), default="Pending")
    priority = Column(String(50), default="Medium")

    project_id = Column(
        Integer,
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False
    )

    assigned_to = Column(
        Integer,
        ForeignKey("employees.id", ondelete="SET NULL"),
        nullable=True
    )

    due_date = Column(Date)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    project = relationship(
        "Project",
        back_populates="tasks"
    )

    employee = relationship(
        "Employee",
        back_populates="tasks"
    )