from __future__ import annotations
from typing import TYPE_CHECKING, Literal, Sequence


from memoryfm.models.service_enums import ChartKindColumn, Frequency
import memoryfm.storage.attachment_index as attrepo
from memoryfm.storage.user_repo import get_user_by_username

if TYPE_CHECKING:
    from sqlalchemy.orm import Session
    from sqlalchemy import RowMapping


def get_renyi_entropy_by_username(
    session: Session,
    username: str,
    kind: ChartKindColumn,
    period: int | Literal["all_time"] = 30,
    freq: Frequency = Frequency.D,
    alpha: float = 1,
) -> Sequence[RowMapping] | None:
    user = get_user_by_username(session, username)
    if user:
        user_id = user.id
        return attrepo.get_renyi_entropy(session, user_id, kind, period, freq, alpha)
    return None


def get_attachment_index_by_username(
    session: Session,
    username: str,
    kind: ChartKindColumn,
    period: int | Literal["all_time"] = 30,
    freq: Frequency = Frequency.D,
    alpha: float = 1,
):
    user = get_user_by_username(session, username)
    if user:
        user_id = user.id
        return attrepo.get_attachment_index(session, user_id, kind, period, freq, alpha)
    return None
