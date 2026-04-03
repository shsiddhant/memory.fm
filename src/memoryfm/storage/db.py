from __future__ import annotations
from typing import TYPE_CHECKING
import logging
from contextlib import contextmanager
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlite3 import Connection as SQLite3Connection

from memoryfm.config import DB_URL
from memoryfm.core.models import Base

if TYPE_CHECKING:
    from sqlalchemy import Engine

engine: Engine = create_engine(DB_URL)

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)


@event.listens_for(engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()


SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def init_db():
    "Initialize database from models schema."
    Base.metadata.create_all(engine)


def startup():
    "Application startup"
    init_db()


@contextmanager
def get_db_session():
    "Get a database session context manager."
    Session = SessionLocal()
    try:
        yield Session
    finally:
        Session.close()
