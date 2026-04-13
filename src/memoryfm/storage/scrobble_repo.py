from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import insert

from memoryfm.models.core import Scrobble

if TYPE_CHECKING:
    from collections.abc import Sequence
    from sqlalchemy.orm import Session
    from datetime import datetime


def get_scrobbles_by_user(
    session: Session, user_id: int, limit: int | None = None, offset: int | None = None
) -> Sequence[Scrobble]:
    stmt = (
        select(Scrobble).where(Scrobble.user_id == user_id).limit(limit).offset(offset)
    )
    return session.scalars(stmt).fetchall()


def insert_scrobbles_by_user(session: Session, user_id: int, scrobbles: Sequence[dict]):
    data = [{**scrobble, "user_id": user_id} for scrobble in scrobbles]
    stmt = insert(Scrobble).on_conflict_do_nothing(
        index_elements=["timestamp", "track", "artist", "album", "user_id"],
    )
    session.execute(stmt, data)


def get_end_timestamps_by_user(
    session: Session, user_id: int
) -> tuple[datetime, datetime] | None:
    stmt = select(func.min(Scrobble.timestamp), func.max(Scrobble.timestamp)).where(
        Scrobble.user_id == user_id
    )
    data = session.execute(stmt).fetchone()
    if data:
        return data.tuple()
    return None
