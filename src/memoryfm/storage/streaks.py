import datetime
from typing import Literal

from sqlalchemy import func, select
from sqlalchemy.orm import Session
import numpy as np

from memoryfm.models.core import Scrobble
from memoryfm.models.service_enums import ChartKindColumn
from memoryfm._cython._streaks import streak_gen


def gen_consecutive_comparison(
    session: Session,
    user_id: int,
    kind: ChartKindColumn,
    from_ts: datetime.datetime | None = None,
    to_ts: datetime.datetime | None = None,
    offset: int = 0,
    limit: int | None = None,
):
    stmt = (
        select(
            Scrobble.id,
            Scrobble.timestamp,
            kind.column,
            (
                kind.column
                == func.lead(kind.column).over(
                    order_by=(Scrobble.timestamp, Scrobble.id)
                )
            ).label("comparison"),
        )
        .where(Scrobble.user_id == user_id)
        .offset(offset)
    )

    if from_ts:
        stmt = stmt.filter(Scrobble.timestamp >= from_ts)
    if to_ts:
        stmt = stmt.filter(Scrobble.timestamp < to_ts)

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
    streaks: list[tuple[datetime.datetime, datetime.datetime, str, int]]
    streaks = [
        (
            consecutive_bool[streaks_data[i, 0]]["timestamp"],  # Streak start timestamp
            consecutive_bool[streaks_data[i, 1]]["timestamp"],  # Streak end timestamp
            consecutive_bool[streaks_data[i, 0]][kind.value],  # Streak value
            streaks_data[i, 2],  # Streak Length
        )
        for i in range(streaks_data.shape[0])
        if consecutive_bool[streaks_data[i, 0]][kind.value]
    ]

    return streaks
