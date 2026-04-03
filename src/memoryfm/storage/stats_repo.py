from __future__ import annotations
from typing import TYPE_CHECKING
import datetime
from sqlalchemy import select, func
from memoryfm.core.models import Scrobble
from memoryfm.storage.user_repo import get_user_by_id

if TYPE_CHECKING:
    from typing import Literal
    from sqlalchemy.orm import Session


def get_summary_by_user(session: Session, user_id: int) -> dict | None:
    user = get_user_by_id(session, user_id)
    username = user.username if user else None
    data = session.execute(
        select(
            func.count(Scrobble.id).label("count"),
            func.min(Scrobble.timestamp).label("first_scrobble"),
            func.max(Scrobble.timestamp).label("last_scrobble"),
        ).where(Scrobble.user_id == user_id)
    ).fetchone()
    if data:
        count, first_date, last_date = data
        if first_date and last_date:
            days = (last_date - first_date).days
            return {
                "user_id": user_id,
                "username": username,
                "count": count,
                "days": days,
            }
    return None


def get_top_charts_by_user(
    session: Session,
    user_id: int,
    kind: Literal["artist", "album", "track"],
    period: int | Literal["all_time"] = 7,
    limit: int | None = 10,
) -> dict:
    if period != "all_time":
        now = datetime.datetime.now()
        datelimit = now - datetime.timedelta(days=period)
    else:
        datelimit = datetime.datetime.fromtimestamp(0)
    if kind == "track":
        col = Scrobble.track
    elif kind == "artist":
        col = Scrobble.artist
    elif kind == "album":
        col = Scrobble.album
    else:
        raise ValueError("Kind must be one of: 'tracks', 'artists', 'albums'")
    data = session.execute(
        select(col, func.count(Scrobble.id).label("scrobbles"))
        .where(Scrobble.user_id == user_id, Scrobble.timestamp >= datelimit)
        .group_by(col)
        .order_by(func.count(Scrobble.id).desc())
        .limit(limit)
    ).fetchall()
    top = {
        kind: [row._mapping[kind] for row in data],
        "scrobbles": [row.scrobbles for row in data],
    }
    return top
