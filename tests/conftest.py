from pathlib import Path

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from testcontainers.postgres import PostgresContainer
from memoryfm.io.lastfmstats import from_lastfmstats
from memoryfm.models.core import Base

data_dir = Path(__file__).resolve().parent / "data"
json_dir = data_dir / "json"
csv_dir = data_dir / "csv"
file = json_dir / "lastfmstats-lazulinoother_test.json"
tz = "Asia/Kolkata"


@pytest.fixture(scope="session")
def postgres_container():
    with PostgresContainer("postgres:16-alpine") as postgres:
        yield postgres


@pytest.fixture(scope="session")
def engine(postgres_container):
    engine = create_engine(postgres_container.get_connection_url())
    Base.metadata.create_all(engine)
    yield engine

    engine.dispose()


@pytest.fixture
def db_session(engine):
    connection = engine.connect()
    transaction = connection.begin()

    SessionLocal = sessionmaker(bind=connection)
    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture
def seeded_db(db_session):
    from_lastfmstats(db_session, file, tz)
    yield db_session
