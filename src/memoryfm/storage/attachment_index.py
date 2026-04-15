from __future__ import annotations
from typing import Literal, TYPE_CHECKING
from math import exp
from sqlalchemy import select, func
from memoryfm.models.service_enums import Frequency
from memoryfm.models.core import Scrobble
from memoryfm.util.datetime_util import get_datelimit_from_period

if TYPE_CHECKING:
    from sqlalchemy.orm import Session
    from memoryfm.models.service_enums import (
        ChartKindColumn,
    )


def get_frequency_counts_cte(
    user_id: int,
    kind: ChartKindColumn,
    period: int | Literal["all_time"] = 30,
    freq: Frequency = Frequency.D,
):
    datelimit = get_datelimit_from_period(period)

    stmt_cte_bin = (
        select(
            func.date_trunc(freq.value, Scrobble.timestamp).label(freq.value),
            kind.column,
        )
        .where(Scrobble.user_id == user_id, Scrobble.timestamp >= datelimit)
        .cte("binned")
    )

    stmt_cte_freq = (
        select(
            stmt_cte_bin.columns[freq.value],
            stmt_cte_bin.columns[kind.value],
            func.count().label("scrobbles"),
        )
        .group_by(freq.value, kind.value)
        .cte("freq")
    )
    return stmt_cte_freq


def get_renyi_entropy(
    session: Session,
    user_id: int,
    kind: ChartKindColumn,
    period: int | Literal["all_time"] = 30,
    freq: Frequency = Frequency.D,
    alpha: float = 1,
):
    stmt_cte_freq = get_frequency_counts_cte(user_id, kind, period, freq)
    cte_freq_cols = stmt_cte_freq.columns
    scrobbles_col = cte_freq_cols["scrobbles"]

    if alpha != 1:
        entropy_col = (1 / (1 - alpha)) * func.ln(
            func.sum(func.pow(scrobbles_col, alpha))
        )
    elif alpha == 1:
        entropy_col = func.ln(func.sum(scrobbles_col)) - (
            func.sum(scrobbles_col * func.ln(scrobbles_col)) / func.sum(scrobbles_col)
        )
    else:
        return None
    stmt = select(
        cte_freq_cols[freq.value].label("day"), entropy_col.label("value")
    ).group_by(freq.value)
    data = session.execute(stmt).mappings().fetchall()
    return data


def get_attachment_index(
    session: Session,
    user_id: int,
    kind: ChartKindColumn,
    period: int | Literal["all_time"] = 30,
    freq: Frequency = Frequency.D,
    alpha: float = 1,
):
    entropy = get_renyi_entropy(session, user_id, kind, period, freq, alpha)
    att_index = (
        [{"day": k["day"], "value": 100 * exp(-k["value"])} for k in entropy]
        if entropy
        else None
    )
    return att_index
