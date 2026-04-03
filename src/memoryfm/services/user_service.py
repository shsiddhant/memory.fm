from __future__ import annotations
from sqlalchemy.exc import SQLAlchemyError
from memoryfm.storage.db import get_db_session
import memoryfm.storage.user_repo as urep
from memoryfm.util.datetime_util import validate_tz


def create_user(
    username: str,
    tz: str | None = "Etc/UTC",
    overwrite: bool = False,
):
    tz = validate_tz(tz)
    with get_db_session() as session:
        try:
            user = urep.get_user_by_username(session, username)
            if overwrite and user:
                urep.delete_user(session, user.id)
            if not user:
                urep.insert_user(session, username, tz)
            session.commit()
        except SQLAlchemyError:
            session.rollback()
            raise
        except Exception:
            raise


def delete_user(user_id: int):
    with get_db_session() as session:
        try:
            urep.delete_user(session, user_id)
            session.commit()
        except SQLAlchemyError:
            session.rollback()
            raise


def get_user_context(username: str) -> dict | None:
    with get_db_session() as session:
        user = urep.get_user_by_username(session, username)
        if user:
            return {"user_id": user.id, "tz": user.tz}
        return None
