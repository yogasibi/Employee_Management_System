""" This module provides database connection and session management """
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings

"""Creates database engine"""
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True
)

"""Creates database sessions"""
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

"""Base class for database models"""
Base = declarative_base()

"""Provides a database session to API requests"""
def get_db():
    db = SessionLocal()

    """yield - Provides the session and allows cleanup afterward
    try/finally - We need to close database connections even when an API request fails"""
    try:yield db
    finally:
        db.close()