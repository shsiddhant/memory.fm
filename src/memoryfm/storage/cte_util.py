import datetime

from sqlalchemy import CTE, Float, func, select

from memoryfm.models.core import AnalyticsView
from memoryfm.models.service_enums import ChartKindColumn, Frequency


def get_frequency_cte(
    user_id: int,
    kind: ChartKindColumn,
    from_ts: datetime.datetime | None = None,
    to_ts: datetime.datetime | None = None,
    freq: Frequency = Frequency.D,
) -> CTE:
    id_col = kind.id_column.label("id")  # type: ignore[attr-defined]
    name_col = kind.name_column.label("name")  # type: ignore[attr-defined]
    subname_col = kind.subname_column.label("subname") if kind.subname_column else None  # type: ignore[attr-defined]
    date_col = func.date_trunc(freq.value, AnalyticsView.timestamp).label(freq.value)

    if subname_col is not None:
        stmt = select(date_col, id_col, name_col, subname_col)
    else:
        stmt = select(date_col, id_col, name_col)

    stmt_bin = stmt.where(AnalyticsView.user_id == user_id)

    if from_ts:
        stmt_bin = stmt_bin.filter(AnalyticsView.timestamp >= from_ts)
    if to_ts:
        stmt_bin = stmt_bin.filter(AnalyticsView.timestamp <= to_ts)

    stmt_cte_bin = stmt_bin.cte("binned")

    columns_new = (
        stmt_cte_bin.columns[freq.value],
        stmt_cte_bin.columns["id"],
        func.any_value(stmt_cte_bin.columns["name"]).label("name"),
        func.count().cast(Float).label("scrobbles"),
    )
    if subname_col is not None:
        stmt = select(
            *columns_new,
            func.any_value(stmt_cte_bin.columns["subname"]).label("subname"),
        )
    else:
        stmt = select(*columns_new)

    stmt_cte_freq = stmt.group_by(
        stmt_cte_bin.columns[freq.value],
        stmt_cte_bin.columns["id"],
    ).cte("freq")
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

    columns = (
        cte_freq_cols[freq.value],
        cte_freq_cols["id"],
        cte_freq_cols["name"],
        total_scrobbles_col.label("total_scrobbles"),
        (scrobbles_col / total_scrobbles_col).label("prop"),
    )

    if kind.subname_column is not None:
        stmt_cte_props = select(*columns, cte_freq_cols["subname"]).cte("props")
    else:
        stmt_cte_props = select(*columns).cte("props")

    stmt_cte_props = select(*columns).cte("props")
    return stmt_cte_props
