from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy.exc import SQLAlchemyError
import memoryfm.storage.user_repo as urepo
from memoryfm.util.datetime_util import validate_tz
from memoryfm.errors import UserNotFoundError
from memoryfm.models.service_helpers import UserContext

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
        user = urepo.get_user_by_username(session, username)
        if overwrite and user:
            urepo.delete_user(session, user.id)
        if not user:
            urepo.insert_user(session, username, tz)
        session.commit()
    except SQLAlchemyError:
        session.rollback()
        raise
    except Exception:
        raise


def delete_user(session: Session, user_id: int):
    try:
        urepo.delete_user(session, user_id)
        session.commit()
    except SQLAlchemyError:
        session.rollback()
        raise


def get_user_context(session: Session, username: str) -> UserContext:
    user = urepo.get_user_by_username(session, username)
    if user:
        return UserContext(user.id, user.tz)
    else:
        raise UserNotFoundError(username)
