import datetime
from typing import Literal

from sqlalchemy import func, select
from sqlalchemy.orm import Session
import numpy as np

from memoryfm.models.core import AnalyticsView
from memoryfm.models.service_enums import ChartKindColumn
from memoryfm._cython._streaks import streak_gen


StreakType = (
    tuple[datetime.datetime, datetime.datetime, str, int, str]
    | tuple[datetime.datetime, datetime.datetime, str, int]
)


def gen_consecutive_comparison(
    session: Session,
    user_id: int,
    kind: ChartKindColumn,
    from_ts: datetime.datetime | None = None,
    to_ts: datetime.datetime | None = None,
    offset: int = 0,
    limit: int | None = None,
):
    scrobble_id_col = AnalyticsView.scrobble_id
    ts_col = AnalyticsView.timestamp
    kind_id_col = kind.id_column.label("kind_id")  # type: ignore[attr-defined]
    name_col = kind.name_column.label("name")  # type: ignore[attr-defined]
    subname_col = kind.subname_column.label("subname") if kind.subname_column else None  # type: ignore[attr-defined]
    comparison_col = (
        kind_id_col == func.lead(kind_id_col).over(order_by=(ts_col, scrobble_id_col))
    ).label("comparison")

    if subname_col is not None:
        stmt = select(
            scrobble_id_col,
            ts_col,
            kind_id_col,
            name_col,
            subname_col,
            comparison_col,
        )
    else:
        stmt = select(
            scrobble_id_col,
            ts_col,
            kind_id_col,
            name_col,
            comparison_col,
        )
    stmt = stmt.where(AnalyticsView.user_id == user_id).offset(offset)

    if from_ts:
        stmt = stmt.filter(AnalyticsView.timestamp >= from_ts)
    if to_ts:
        stmt = stmt.filter(AnalyticsView.timestamp <= to_ts)

    if limit:
        stmt = stmt.limit(limit)

    data = session.execute(stmt).mappings().fetchall()
    return data


def get_streaks(
    session: Session,
    user_id: int,
    kind: ChartKindColumn,
    from_ts: datetime.datetime | None = None,
    to_ts: datetime.datetime | None = None,
    min_length: int = 2,
):
    consecutive_bool = gen_consecutive_comparison(
        session,
        user_id,
        kind,
        from_ts,
        to_ts,
    )
    streak_start = np.array(
        [
            item["comparison"]
            for item in consecutive_bool
            if item["comparison"] is not None
        ],
        dtype=np.int8,
    )
    streaks_data: np.ndarray[tuple[Literal[3], int], np.dtype[np.int32]] = np.asarray(
        streak_gen(streak_start, min_length)
    )
    streaks: list[StreakType]

    def get_streak_values_from_id(i: int) -> StreakType:
        values = (
            consecutive_bool[streaks_data[i, 0]]["timestamp"],  # Streak start timestamp
            consecutive_bool[streaks_data[i, 1]]["timestamp"],  # Streak end timestamp
            consecutive_bool[streaks_data[i, 0]]["name"],  # Streak name
            streaks_data[i, 2],  # Streak Length
        )
        if "subname" in consecutive_bool[streaks_data[i, 0]]:
            return (*values, consecutive_bool[streaks_data[i, 0]]["subname"])
        return values

    streaks = [
        get_streak_values_from_id(i)
        for i in range(streaks_data.shape[0])
        if consecutive_bool[streaks_data[i, 0]]["name"]
    ]

    return streaks
