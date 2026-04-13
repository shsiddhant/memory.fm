from __future__ import annotations
from typing import TYPE_CHECKING
import logging
from sqlalchemy.exc import SQLAlchemyError
import memoryfm.storage.user_repo as urepo
from memoryfm.util.datetime_util import validate_tz
from memoryfm.errors import UserNotFoundError
from memoryfm.models.service_helpers import UserContext
from memoryfm.models.sync_status import UserExist

if TYPE_CHECKING:
    from sqlalchemy.orm import Session
    from memoryfm.models.sync_status import EnsureUserStatus


logger = logging.getLogger(__name__)


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


def ensure_user(session: Session, username: str, ensure_user_status: EnsureUserStatus):
    ensure_user_status.status = UserExist.Checking
    try:
        create_user(session, username)
        ensure_user_status.status = UserExist.Exists
    except Exception as e:
        ensure_user_status.status = UserExist.Error
        raise UserNotFoundError(username, *e.args)
