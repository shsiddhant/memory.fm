from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy.exc import SQLAlchemyError
import memoryfm.storage.user_repo as urep
from memoryfm.util.datetime_util import validate_tz

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


def create_user(
    session: Session,
    username: str,
    tz: str | None = "Etc/UTC",
    overwrite: bool = False,
):
    tz = validate_tz(tz)
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


def delete_user(session: Session, user_id: int):
    try:
        urep.delete_user(session, user_id)
        session.commit()
    except SQLAlchemyError:
        session.rollback()
        raise


def get_user_context(session: Session, username: str) -> dict | None:
    user = urep.get_user_by_username(session, username)
    if user:
        return {"user_id": user.id, "tz": user.tz}
    return None
