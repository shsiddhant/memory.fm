from __future__ import annotations
from typing import TYPE_CHECKING
import datetime
from sqlalchemy import desc, distinct, select, func
from memoryfm.models.core import AnalyticsView
from memoryfm.models.service_enums import Frequency
from memoryfm.storage.user_repo import get_user_by_id
from memoryfm.storage.cte_util import get_frequency_cte

if TYPE_CHECKING:
    from typing import Sequence
    from sqlalchemy.orm import Session
    from sqlalchemy import RowMapping
    from memoryfm.models.service_enums import ChartKindColumn


def get_summary_by_user(session: Session, user_id: int) -> dict | None:
    user = get_user_by_id(session, user_id)
    username = user.username if user else None

    columns = (
        func.count(AnalyticsView.scrobble_id).label("count"),
        func.min(AnalyticsView.timestamp).label("first_scrobble"),
        func.max(AnalyticsView.timestamp).label("last_scrobble"),
        func.count(distinct(AnalyticsView.track_id)).label("tracks"),
        func.count(distinct(AnalyticsView.artist_id)).label("artists"),
        func.count(distinct(AnalyticsView.album_id))
        .filter(AnalyticsView.album != "")
        .label("albums"),
    )
    conditions = [AnalyticsView.user_id == user_id]
    stmt = select(*columns).where(*conditions)

    data = session.execute(stmt).mappings().fetchone()

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
    kind: ChartKindColumn,
    from_ts: datetime.datetime | None = None,
    to_ts: datetime.datetime | None = None,
    limit: int | None = 10,
) -> Sequence[RowMapping]:
    id_col = kind.id_column.label("id")  # type: ignore[attr-defined]
    name_col = func.any_value(kind.name_column).label("name")
    subname_col = func.any_value(kind.subname_column).label("subname")
    scrobbles_col = func.count(AnalyticsView.scrobble_id).label("scrobbles")

    stmt = select(id_col, name_col, scrobbles_col)
    if subname_col is not None:
        stmt = select(id_col, name_col, subname_col, scrobbles_col)

    conditions = (AnalyticsView.user_id == user_id,)
    groupby = (id_col,)
    orderby = (desc(scrobbles_col), desc(func.max(AnalyticsView.timestamp)))

    stmt = stmt.where(*conditions).group_by(*groupby).order_by(*orderby).limit(limit)

    if from_ts:
        stmt = stmt.filter(AnalyticsView.timestamp >= from_ts)
    if to_ts:
        stmt = stmt.filter(AnalyticsView.timestamp <= to_ts)

    top = session.execute(stmt).mappings().fetchall()
    return top


def get_daily_scrobbles_count(
    session: Session,
    user_id: int,
    till: datetime.date | None = None,
    limit: int = 56,
) -> tuple[datetime.date, datetime.date, Sequence[RowMapping]]:
    datelimit = till if till else datetime.date.today()
    to_date = datelimit
    from_date = to_date - datetime.timedelta(days=limit)

    date_col = func.date(AnalyticsView.timestamp)
    columns = [
        date_col.label("Date"),
        func.count(AnalyticsView.scrobble_id).label("Scrobbles"),
    ]
    conditions = [
        AnalyticsView.user_id == user_id,
        func.date(AnalyticsView.timestamp) <= to_date,
        func.date(AnalyticsView.timestamp) >= from_date,
    ]
    orderby = (desc(date_col),)
    groupby = (date_col,)
    stmt = select(*columns).where(*conditions).order_by(*orderby).group_by(*groupby)

    data = session.execute(stmt).mappings().all()
    return from_date, to_date, data


def get_top_charts_by_freq(
    session: Session,
    user_id: int,
    kind: ChartKindColumn,
    from_ts: datetime.datetime | None = None,
    to_ts: datetime.datetime | None = None,
    freq: Frequency = Frequency.D,
) -> Sequence[RowMapping]:
    stmt_cte_freq = get_frequency_cte(user_id, kind, from_ts, to_ts, freq)
    cols = stmt_cte_freq.columns
    scrobbles_col = cols["scrobbles"]
    total_scrobbles_col = func.sum(scrobbles_col).over(partition_by=cols[freq.value])
    stmt = (
        select(
            cols[freq.value].label("day"),
            cols[kind.value].label("name"),
            cols["scrobbles"],
            total_scrobbles_col.label("total_scrobbles"),
        )
        .distinct(cols[freq.value])
        .order_by(cols[freq.value], desc(cols["scrobbles"]))
    )
    top = session.execute(stmt).mappings().fetchall()
    return top
