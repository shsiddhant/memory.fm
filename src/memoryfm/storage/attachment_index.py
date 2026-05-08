from __future__ import annotations
from typing import TYPE_CHECKING, Sequence
from math import exp
from sqlalchemy import select, func
from memoryfm.models.service_enums import Frequency
from memoryfm.storage.cte_util import get_frequency_proportions_cte

if TYPE_CHECKING:
    import datetime
    from sqlalchemy.orm import Session
    from sqlalchemy import RowMapping
    from memoryfm.models.service_enums import (
        ChartKindColumn,
    )


def get_renyi_entropy(
    session: Session,
    user_id: int,
    kind: ChartKindColumn,
    from_ts: datetime.datetime | None = None,
    to_ts: datetime.datetime | None = None,
    freq: Frequency = Frequency.D,
    alpha: float = 1,
    tz: str = "Etc/UTC",
) -> Sequence[RowMapping] | None:
    stmt_cte_props = get_frequency_proportions_cte(
        user_id, kind, from_ts, to_ts, freq, tz
    )
    cte_props_cols = stmt_cte_props.columns
    prop_col = cte_props_cols["prop"]
    total_scrobbles_col = func.any_value(cte_props_cols["total_scrobbles"])

    if alpha != 1:
        entropy_col = (1 / (1 - alpha)) * func.ln(func.sum(func.pow(prop_col, alpha)))
    elif alpha == 1:
        entropy_col = -func.sum(prop_col * func.ln(prop_col))
    else:
        return None
    stmt = select(
        cte_props_cols[freq.value].label("day"),
        total_scrobbles_col.label("total_scrobbles"),
        entropy_col.label("value"),
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
    tz: str = "Etc/UTC",
):
    entropy = get_renyi_entropy(session, user_id, kind, from_ts, to_ts, freq, alpha, tz)
    att_index = (
        [{"day": k["day"], "value": 100 * exp(-k["value"])} for k in entropy]
        if entropy
        else None
    )
    return att_index
