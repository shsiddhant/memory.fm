from __future__ import annotations
from sqlalchemy.orm import sessionmaker

from memoryfm.storage.engine import engine
from memoryfm.models.core import Base


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
