from __future__ import annotations
from typing import TYPE_CHECKING
import logging
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from memoryfm.core.models import Scrobble, User
from memoryfm.db import get_db_session

if TYPE_CHECKING:
    from collections.abc import Sequence

logger = logging.getLogger("sqlalchemy.engine")


def create_user(
    username: str, tz: str | None = "Etc/UTC", scrobbles: list[Scrobble] = []
):
    user = User(username=username, tz=tz, scrobbles=scrobbles)
    with get_db_session() as session:
        try:
            session.add(user)
            session.commit()
        except SQLAlchemyError:
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


def delete_user(user_id: int):
    with get_db_session() as session:
        try:
            user = session.get(User, user_id)
            if user:
                session.delete(user)
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


def insert_scrobbles(user_id: int, scrobbles: Sequence[dict], chunk_size: int = 1000):
    def get_chunks():
        n = len(scrobbles)
        i = 0
        while i < n:
            yield scrobbles[i : i + chunk_size] if i + chunk_size < n else scrobbles[i:]
            i += chunk_size

    with get_db_session() as session:
        user = session.get(User, user_id)
        for chunk in get_chunks():
            try:
                scrobble_objs = [
                    Scrobble(
                        timestamp=scrobble["timestamp"],
                        track=scrobble["track"],
                        artist=scrobble["artist"],
                        album=scrobble["album"],
                    )
                    for scrobble in chunk
                ]
                if user:
                    user.scrobbles.extend(scrobble_objs)
                    logger.info("Appended %s scrobbles", len(scrobble_objs))
                else:
                    logger.error("User id not found.")
                session.commit()
            except SQLAlchemyError:
                session.rollback()
                raise
