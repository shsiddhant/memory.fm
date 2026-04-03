from __future__ import annotations
from typing import Literal
import datetime
from sqlalchemy import select, func
from memoryfm.core.models import Scrobble, User
from memoryfm.db import get_db_session


def get_user_summary(username: str):
    with get_db_session() as session:
        data = session.execute(
            select(
                User.id,
                func.count(Scrobble.id).label("count"),
                func.min(Scrobble.timestamp).label("first_scrobble"),
                func.max(Scrobble.timestamp).label("last_scrobble"),
            )
            .join(Scrobble)
            .where(User.username == username)
        ).fetchone()
        if data:
            user_id, count, first_date, last_date = data
            if first_date and last_date:
                days = (last_date - first_date).days
                return {
                    "user_id": user_id,
                    "username": username,
                    "count": count,
                    "days": days,
                }


def get_max_timestamp(user_id: int):
    with get_db_session() as session:
        timestamp = session.scalar(
            select(func.max(Scrobble.timestamp)).where(Scrobble.user_id == user_id)
        )
        return timestamp


def get_top_charts(
    username: str,
    kind: Literal["artist", "album", "track"],
    period: int | Literal["all_time"] = 7,
    limit: int | None = 10,
):
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
    with get_db_session() as session:
        data = session.execute(
            select(col, func.count(Scrobble.id).label("scrobbles"))
            .join(User)
            .where(User.username == username, Scrobble.timestamp >= datelimit)
            .group_by(col)
            .order_by(func.count(Scrobble.id).desc())
            .limit(limit)
        ).fetchall()
        top = {
            kind: [row._mapping[kind] for row in data],
            "scrobbles": [row.scrobbles for row in data],
        }
        return top
