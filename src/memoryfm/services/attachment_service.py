from __future__ import annotations
from typing import TYPE_CHECKING, Sequence
import pandas as pd
import numpy as np

from memoryfm.models.service_enums import ChartKindColumn, Frequency
import memoryfm.storage.attachment_index as attrepo
from memoryfm.storage.user_repo import get_user_by_username

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
