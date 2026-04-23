from __future__ import annotations
from typing import TYPE_CHECKING, Literal, Sequence
import pandas as pd
import numpy as np

from memoryfm.models.service_enums import ChartKindColumn, Frequency
import memoryfm.storage.attachment_index as attrepo
from memoryfm.storage.user_repo import get_user_by_username
from memoryfm.storage.stats_repo import get_top_charts_by_freq
from memoryfm.util.datetime_util import get_datelimit_from_period, normalize_timestamp

if TYPE_CHECKING:
    import datetime
    from sqlalchemy.orm import Session
    from sqlalchemy import RowMapping


def get_renyi_entropy_by_username(
    session: Session,
    username: str,
    kind: ChartKindColumn,
    from_ts: datetime.datetime | None = None,
    to_ts: datetime.datetime | None = None,
    freq: Frequency = Frequency.D,
    alpha: float = 1,
) -> Sequence[RowMapping] | None:
    user = get_user_by_username(session, username)
    if user:
        user_id = user.id
        return attrepo.get_renyi_entropy(
            session, user_id, kind, from_ts, to_ts, freq, alpha
        )
    return None


def get_attachment_index_by_username(
    session: Session,
    username: str,
    kind: ChartKindColumn,
    from_ts: datetime.datetime | None = None,
    to_ts: datetime.datetime | None = None,
    freq: Frequency = Frequency.D,
    alpha: float = 1,
):
    user = get_user_by_username(session, username)
    if user:
        user_id = user.id
        return attrepo.get_attachment_index(
            session, user_id, kind, from_ts, to_ts, freq, alpha
        )
    return None


def get_weighted_attachment_index_by_username(
    session: Session,
    username: str,
    kind: ChartKindColumn,
    from_ts: datetime.datetime | None = None,
    to_ts: datetime.datetime | None = None,
    freq: Frequency = Frequency.D,
    alpha: float = 1,
):
    user = get_user_by_username(session, username)
    if user:
        user_id = user.id
        entropy = attrepo.get_renyi_entropy(
            session, user_id, kind, from_ts, to_ts, freq, alpha
        )
        if entropy:
            df = pd.DataFrame(entropy)
            max = df.total_scrobbles.max()
            df["weight"] = np.log1p(df.total_scrobbles / max) / np.log(2)
            df["value"] = 100 * df["weight"] * np.exp(-df["value"])
            df["day"] = df["day"].dt.to_pydatetime()
            return df[["day", "value"]].to_dict(orient="records")
        return None


def get_attachment_moments(
    session: Session,
    username: str,
    kind: ChartKindColumn,
    from_ts: datetime.datetime | None = None,
    to_ts: datetime.datetime | None = None,
    freq: Frequency = Frequency.D,
    alpha: float = 1,
    threshold: float = 1,
):
    user = get_user_by_username(session, username)
    if user:
        user_id = user.id
        weighted_att = get_weighted_attachment_index_by_username(
            session,
            username,
            kind,
            from_ts,
            to_ts,
            freq,
            alpha,
        )
        top_charts = get_top_charts_by_freq(
            session, user_id, kind, from_ts, to_ts, freq
        )
        if weighted_att and top_charts:
            df = pd.DataFrame(weighted_att)
            top_charts_df = pd.DataFrame(top_charts)
            df["z_score"] = (df["value"] - df["value"].mean()) / df["value"].std()

            top_moments_df = df[df["z_score"] >= threshold]
            top_moments_df["day"] = top_moments_df["day"].dt.strftime("%Y-%m-%d")
            top_moments_df[["name", "scrobbles", "total_scrobbles"]] = top_charts_df[
                ["name", "scrobbles", "total_scrobbles"]
            ]
            top_moments_df["dominance"] = (
                top_moments_df["scrobbles"] / top_moments_df["total_scrobbles"]
            )
            return top_moments_df.to_dict(orient="records")
        return None


def get_attachment_moments_by_period(
    session: Session,
    username: str,
    kind: ChartKindColumn,
    period: int | Literal["all_time"],
    freq: Frequency = Frequency.D,
    alpha: float = 1,
    threshold: float = 1,
):
    user = get_user_by_username(session, username)
    if user:
        tz = user.tz
        from_ts = normalize_timestamp(get_datelimit_from_period(period), tz)
        return get_attachment_moments(
            session,
            username,
            kind,
            from_ts,
            to_ts=None,
            freq=freq,
            alpha=alpha,
            threshold=threshold,
        )
    return None
