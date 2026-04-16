from __future__ import annotations
from typing import TYPE_CHECKING, Literal
from memoryfm.storage.user_repo import get_user_by_username
import memoryfm.storage.stats_repo as strepo
from memoryfm.util.datetime_util import get_datelimit_from_period

if TYPE_CHECKING:
    from typing import Sequence
    import datetime
    from sqlalchemy import RowMapping
    from sqlalchemy.orm import Session
    from memoryfm.models.service_enums import ChartKindColumn


def get_summary_by_username(session: Session, username: str) -> dict | None:
    user = get_user_by_username(session, username)
    if user:
        user_id = user.id
        return strepo.get_summary_by_user(session, user_id)
    return None


def get_top_charts_by_username(
    session: Session,
    username: str,
    kind: ChartKindColumn,
    from_ts: datetime.datetime | None = None,
    to_ts: datetime.datetime | None = None,
    limit: int | None = 10,
) -> Sequence[RowMapping] | None:
    user = get_user_by_username(session, username)
    if user:
        user_id = user.id
        return strepo.get_top_charts_by_user(
            session, user_id, kind, from_ts, to_ts, limit
        )
    return None


def get_top_charts_by_period(
    session: Session,
    username: str,
    kind: ChartKindColumn,
    period: int | Literal["all_time"],
    limit: int | None = 10,
) -> Sequence[RowMapping] | None:
    from_ts = get_datelimit_from_period(period)
    return get_top_charts_by_username(session, username, kind, from_ts, limit=limit)


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
