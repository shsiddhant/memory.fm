from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from memoryfm.config import DB_URL
from memoryfm.models.core import Base

if TYPE_CHECKING:
    from sqlalchemy import Engine

engine: Engine = create_engine(DB_URL, pool_size=5, max_overflow=10, pool_pre_ping=True)


SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def init_db():
    "Initialize database from models schema."
    Base.metadata.create_all(engine)


def get_db_session():
    "Get a database session context manager."
    Session = SessionLocal()
    try:
        yield Session
    finally:
        Session.close()
