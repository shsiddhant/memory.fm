from __future__ import annotations
from typing import TYPE_CHECKING, Sequence
from math import exp
from sqlalchemy import select, func, Float
from memoryfm.models.service_enums import Frequency
from memoryfm.models.core import Scrobble

if TYPE_CHECKING:
    import datetime
    from sqlalchemy.orm import Session
    from sqlalchemy import RowMapping
    from memoryfm.models.service_enums import (
        ChartKindColumn,
    )


def get_frequency_proportions_cte(
    user_id: int,
    kind: ChartKindColumn,
    from_ts: datetime.datetime | None = None,
    to_ts: datetime.datetime | None = None,
    freq: Frequency = Frequency.D,
):
    stmt_bin = select(
        func.date_trunc(freq.value, Scrobble.timestamp).label(freq.value),
        kind.column,
    ).where(Scrobble.user_id == user_id)
    if from_ts:
        stmt_bin = stmt_bin.filter(Scrobble.timestamp >= from_ts)
    if to_ts:
        stmt_bin = stmt_bin.filter(Scrobble.timestamp < to_ts)

    stmt_cte_bin = stmt_bin.cte("binned")

    stmt_cte_freq = (
        select(
            stmt_cte_bin.columns[freq.value],
            stmt_cte_bin.columns[kind.value],
            func.count().cast(Float).label("scrobbles"),
        )
        .group_by(
            stmt_cte_bin.columns[freq.value],
            stmt_cte_bin.columns[kind.value],
        )
        .cte("freq")
    )
    cte_freq_cols = stmt_cte_freq.columns
    scrobbles_col = cte_freq_cols["scrobbles"]
    stmt_cte_props = select(
        cte_freq_cols[freq.value],
        cte_freq_cols[kind.value],
        (
            scrobbles_col
            / func.sum(scrobbles_col).over(partition_by=cte_freq_cols[freq.value])
        ).label("prop"),
    ).cte("props")
    return stmt_cte_props


def get_renyi_entropy(
    session: Session,
    user_id: int,
    kind: ChartKindColumn,
    from_ts: datetime.datetime | None = None,
    to_ts: datetime.datetime | None = None,
    freq: Frequency = Frequency.D,
    alpha: float = 1,
) -> Sequence[RowMapping] | None:
    stmt_cte_props = get_frequency_proportions_cte(user_id, kind, from_ts, to_ts, freq)
    cte_props_cols = stmt_cte_props.columns
    prop_col = cte_props_cols["prop"]

    if alpha != 1:
        entropy_col = (1 / (1 - alpha)) * func.ln(func.sum(func.pow(prop_col, alpha)))
    elif alpha == 1:
        entropy_col = -func.sum(prop_col * func.ln(prop_col))
    else:
        return None
    stmt = select(
        cte_props_cols[freq.value].label("day"), entropy_col.label("value")
    ).group_by(cte_props_cols[freq.value])
    data = session.execute(stmt).mappings().fetchall()
    return data


def get_attachment_index(
    session: Session,
    user_id: int,
    kind: ChartKindColumn,
    from_ts: datetime.datetime | None = None,
    to_ts: datetime.datetime | None = None,
    freq: Frequency = Frequency.D,
    alpha: float = 1,
):
    entropy = get_renyi_entropy(session, user_id, kind, from_ts, to_ts, freq, alpha)
    att_index = (
        [{"day": k["day"], "value": 100 * exp(-k["value"])} for k in entropy]
        if entropy
        else None
    )
    return att_index
