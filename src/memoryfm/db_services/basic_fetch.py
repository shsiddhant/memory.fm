from __future__ import annotations
from typing import TYPE_CHECKING
import logging
from sqlalchemy import select, delete
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from memoryfm.core.models import Scrobble, User
from memoryfm.db import get_db_session

if TYPE_CHECKING:
    from collections.abc import Sequence

logger = logging.getLogger("sqlalchemy.engine")


def create_user(
    username: str,
    tz: str | None = "Etc/UTC",
    overwrite: bool = False,
):
    user_id = get_userid_from_username(username)
    data = {"username": username, "tz": tz}
    with get_db_session() as session:
        if overwrite and user_id:
            delete_user(user_id)
        elif not user_id:
            stmt = insert(User).values(data)
            try:
                session.execute(stmt)
                session.commit()
            except (IntegrityError, SQLAlchemyError):
                session.rollback()
                raise


def get_user(user_id: int) -> User | None:
    with get_db_session() as session:
        try:
            user = session.get(User, user_id)
            return user
        except SQLAlchemyError:
            raise
        except Exception:
            raise


def get_userid_from_username(username: str) -> int | None:
    with get_db_session() as session:
        stmt = select(User.id).where(User.username == username)
        user_id = session.scalar(stmt)
        return user_id


def get_user_tz(user_id: int) -> str | None:
    with get_db_session() as session:
        tz = session.scalar(select(User.tz).where(User.id == user_id))
        return tz


def delete_user(user_id: int):
    with get_db_session() as session:
        stmt = delete(User).where(User.id == user_id)
        try:
            session.execute(stmt)
            session.commit()
        except SQLAlchemyError:
            session.rollback()
            raise
        except Exception:
            raise


def get_scrobbles_from_username(
    username: str, limit: int | None = None, offset: int | None = None
) -> Sequence[Scrobble]:
    with get_db_session() as session:
        try:
            user_id = session.scalar(select(User.id).where(User.username == username))
            stmt = (
                select(Scrobble)
                .where(Scrobble.user_id == user_id)
                .limit(limit)
                .offset(offset)
            )
            scrobbles = session.scalars(stmt).fetchall()
            return scrobbles
        except SQLAlchemyError:
            raise
        except Exception:
            raise


def insert_scrobbles(user_id: int, scrobbles: Sequence[dict], chunk_size: int = 500):
    def get_chunks():
        n = len(scrobbles)
        i = 0
        while i < n:
            yield scrobbles[i : i + chunk_size]
            i += chunk_size

    for chunk in get_chunks():
        with get_db_session() as session:
            try:
                data = [{**scrobble, "user_id": user_id} for scrobble in chunk]
                stmt = insert(Scrobble)
                upsert_stmt = stmt.on_conflict_do_nothing(
                    index_elements=["timestamp", "track", "artist", "album", "user_id"],
                )
                session.execute(upsert_stmt, data)
                session.commit()
            except SQLAlchemyError:
                session.rollback()
                raise
