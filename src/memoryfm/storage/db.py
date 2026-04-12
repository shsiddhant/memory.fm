from __future__ import annotations
from typing import TYPE_CHECKING
import logging
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from memoryfm.config import DB_URL
from memoryfm.core.models import Base

if TYPE_CHECKING:
    from sqlalchemy import Engine

engine: Engine = create_engine(DB_URL)

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)


SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def init_db():
    "Initialize database from models schema."
    Base.metadata.create_all(engine)


@contextmanager
def get_db_session():
    "Get a database session context manager."
    Session = SessionLocal()
    try:
        yield Session
    finally:
        Session.close()
