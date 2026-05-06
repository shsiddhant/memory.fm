from pathlib import Path
import pytest
from sqlalchemy import create_engine, DDL
from sqlalchemy.orm import sessionmaker
from testcontainers.postgres import PostgresContainer
from memoryfm.io.lastfmstats import from_lastfmstats
from memoryfm.models.core import Base


data_dir = Path(__file__).resolve().parent / "data"
json_dir = data_dir / "json"
csv_dir = data_dir / "csv"
file = json_dir / "fiona.json"
tz = "Asia/Kolkata"


@pytest.fixture(scope="session")
def postgres_container():
    with PostgresContainer("postgres:16-alpine") as postgres:
        yield postgres


@pytest.fixture(scope="session")
def engine(postgres_container):
    engine = create_engine(postgres_container.get_connection_url())

    view_name = "analytics_view"
    view_table = Base.metadata.tables.get(view_name)

    if view_table is not None:
        Base.metadata._remove_table(view_name, schema=view_table.schema)

    Base.metadata.create_all(engine)

    if view_table is not None:
        Base.metadata.tables._insert_item(view_name, view_table)

    view_ddl = DDL("""
        CREATE VIEW analytics_view AS
        SELECT
            s.id AS scrobble_id,
            s.timestamp,
            u.id AS user_id,
            u.username,
            t.id AS track_id,
            t.name AS track,
            al.id AS album_id,
            al.name AS album,
            ar.id AS artist_id,
            ar.name AS artist
        FROM scrobbles s
        JOIN users u ON s.user_id = u.id
        JOIN tracks t ON s.track_id = t.id
        JOIN albums al ON t.album_id = al.id
        JOIN artists ar ON t.artist_id = ar.id
    """)

    with engine.connect() as conn:
        conn.execute(view_ddl)
        conn.commit()

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
