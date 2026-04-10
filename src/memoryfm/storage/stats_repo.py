from __future__ import annotations
from typing import TYPE_CHECKING
import datetime
from sqlalchemy import distinct, select, func
from memoryfm.core.models import Scrobble
from memoryfm.storage.user_repo import get_user_by_id

if TYPE_CHECKING:
    from typing import Literal, Sequence
    from sqlalchemy.orm import Session
    from sqlalchemy import RowMapping


def get_summary_by_user(session: Session, user_id: int) -> dict | None:
    user = get_user_by_id(session, user_id)
    username = user.username if user else None
    data = (
        session.execute(
            select(
                func.count(Scrobble.id).label("count"),
                func.min(Scrobble.timestamp).label("first_scrobble"),
                func.max(Scrobble.timestamp).label("last_scrobble"),
                func.count(distinct(Scrobble.track)).label("tracks"),
                func.count(distinct(Scrobble.artist)).label("artists"),
                func.count(distinct(Scrobble.album)).label("albums"),
            ).where(Scrobble.user_id == user_id)
        )
        .mappings()
        .fetchone()
    )
    if data:
        first_date: datetime.datetime | None = data.get("first_scrobble")
        last_date: datetime.datetime | None = data.get("last_scrobble")
        count = data.get("count")
        if first_date and last_date:
            days = (last_date.date() - first_date.date()).days + 1
            return {
                "user": {
                    "user_id": user_id,
                    "username": username,
                },
                "summary": {
                    "total_scrobbles": count,
                    "days": days,
                    "scrobbling_since": first_date.date().strftime("%B %d, %Y"),
                    "scrobbles_per_day": count // days if count else None,
                    "tracks": data.get("tracks"),
                    "artists": data.get("artists"),
                    "albums": data.get("albums"),
                },
            }
    return None


def get_top_charts_by_user(
    session: Session,
    user_id: int,
    kind: Literal["artist", "album", "track"],
    period: int | Literal["all_time"] = 7,
    limit: int | None = 10,
) -> list:
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
        select(col.label("name"), func.count(Scrobble.id).label("scrobbles"))
        .where(Scrobble.user_id == user_id, Scrobble.timestamp >= datelimit)
        .group_by(col)
        .order_by(func.count(Scrobble.id).desc())
        .limit(limit)
    )
    top = list(data.mappings())
    return top


def get_daily_scrobbles_count(
    session: Session,
    user_id: int,
    till: datetime.date | None = None,
    limit: int = 56,
) -> Sequence[RowMapping]:
    datelimit = till if till else datetime.date.today()
    stmt = (
        select(
            func.date(Scrobble.timestamp).label("Date"),
            func.count(Scrobble.id).label("Scrobbles"),
        )
        .where(Scrobble.user_id == user_id, func.date(Scrobble.timestamp) <= datelimit)
        .order_by(Scrobble.timestamp.desc())
        .group_by("Date")
        .limit(limit)
    )
    data = session.execute(stmt).mappings().all()
    return data
