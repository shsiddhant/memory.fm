from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy import delete, select
from sqlalchemy.dialects.sqlite import insert

from memoryfm.core.models import User

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


def insert_user(
    session: Session,
    username: str,
    tz: str | None = "Etc/UTC",
):
    data = {"username": username, "tz": tz}
    stmt = insert(User).values(data)
    session.execute(stmt)


def get_user_by_id(session: Session, user_id: int) -> User | None:
    return session.get(User, user_id)


def get_user_by_username(session: Session, username: str) -> User | None:
    return session.scalar(select(User).where(User.username == username))


def delete_user(session: Session, user_id: int):
    session.execute(delete(User).where(User.id == user_id))
