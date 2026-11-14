from sqlalchemy import Table, Column, ForeignKey, Integer

from app.database.connection import Base

project_members = Table(
    "project_members",
    Base.metadata,

    Column(
        "project_id",
        Integer,
        ForeignKey("projects.id", ondelete="CASCADE"),
        primary_key=True
    ),

    Column(
        "employee_id",
        Integer,
        ForeignKey("employees.id", ondelete="CASCADE"),
        primary_key=True
    )
)