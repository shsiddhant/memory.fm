from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy.exc import SQLAlchemyError
import memoryfm.storage.scrobble_repo as screpo
from memoryfm.storage.user_repo import get_user_by_username

if TYPE_CHECKING:
    from collections.abc import Sequence
    from datetime import datetime
    from sqlalchemy.orm import Session


def insert_scrobbles(
    session: Session, user_id: int, scrobbles: Sequence[dict], chunk_size: int = 500
):
    def get_chunks():
        n = len(scrobbles)
        i = 0
        while i < n:
            yield scrobbles[i : i + chunk_size]
            i += chunk_size

    for chunk in get_chunks():
        try:
            screpo.insert_scrobbles_by_user(session, user_id, chunk)
            session.commit()
        except SQLAlchemyError:
            session.rollback()
            raise
        except Exception:
            raise


def get_end_timestamps(
    session: Session, user_id: int
) -> tuple[datetime, datetime] | None:
    return screpo.get_end_timestamps_by_user(session, user_id)


def get_year_range(session: Session, username: str):
    user = get_user_by_username(session, username)
    start, end = None, None
    if user:
        user_id = user.id
        timestamps = get_end_timestamps(session, user_id)
        if timestamps:
            start_ts, end_ts = timestamps
            if start_ts:
                start = start_ts.year
            if end_ts:
                end = end_ts.year
    return {"start": start, "end": end}
