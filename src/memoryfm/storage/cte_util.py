import datetime

from sqlalchemy import CTE, Float, func, select

from memoryfm.models.core import Scrobble
from memoryfm.models.service_enums import ChartKindColumn, Frequency


def get_frequency_cte(
    user_id: int,
    kind: ChartKindColumn,
    from_ts: datetime.datetime | None = None,
    to_ts: datetime.datetime | None = None,
    freq: Frequency = Frequency.D,
) -> CTE:
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
    return stmt_cte_freq


def get_frequency_proportions_cte(
    user_id: int,
    kind: ChartKindColumn,
    from_ts: datetime.datetime | None = None,
    to_ts: datetime.datetime | None = None,
    freq: Frequency = Frequency.D,
) -> CTE:
    stmt_cte_freq = get_frequency_cte(user_id, kind, from_ts, to_ts, freq)
    cte_freq_cols = stmt_cte_freq.columns
    scrobbles_col = cte_freq_cols["scrobbles"]
    total_scrobbles_col = func.sum(scrobbles_col).over(
        partition_by=cte_freq_cols[freq.value]
    )
    stmt_cte_props = select(
        cte_freq_cols[freq.value],
        cte_freq_cols[kind.value],
        total_scrobbles_col.label("total_scrobbles"),
        (scrobbles_col / total_scrobbles_col).label("prop"),
    ).cte("props")
    return stmt_cte_props
