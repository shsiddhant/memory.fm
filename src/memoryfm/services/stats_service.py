from __future__ import annotations
from typing import TYPE_CHECKING
from memoryfm.storage.user_repo import get_user_by_username
import memoryfm.storage.stats_repo as strepo

if TYPE_CHECKING:
    from typing import Literal, Sequence
    import datetime
    from sqlalchemy import RowMapping
    from sqlalchemy.orm import Session


def get_summary_by_username(session: Session, username: str) -> dict | None:
    user = get_user_by_username(session, username)
    if user:
        user_id = user.id
        return strepo.get_summary_by_user(session, user_id)
    return None


def get_top_charts_by_username(
    session: Session,
    username: str,
    kind: Literal["artist", "album", "track"],
    period: int | Literal["all_time"] = 7,
    limit: int | None = 10,
) -> list | None:
    user = get_user_by_username(session, username)
    if user:
        user_id = user.id
        return strepo.get_top_charts_by_user(session, user_id, kind, period, limit)
    return None


def get_daily_scrobbles_count(
    session: Session,
    username: str,
    till: datetime.date | None = None,
    limit: int = 56,
) -> tuple[datetime.date, datetime.date, Sequence[RowMapping]] | None:
    user = get_user_by_username(session, username)
    if user:
        user_id = user.id
        return strepo.get_daily_scrobbles_count(session, user_id, till, limit)
    return None
