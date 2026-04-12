from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy.exc import SQLAlchemyError
import memoryfm.storage.scrobble_repo as screpo

if TYPE_CHECKING:
    from collections.abc import Sequence
    from datetime import datetime
    from sqlalchemy.orm import Session


def insert_scrobbles(
    session: Session, user_id: int, scrobbles: Sequence[dict], chunk_size: int = 500
):
    def get_chunks():
        n = len(scrobbles)
        i = 0
        while i < n:
            yield scrobbles[i : i + chunk_size]
            i += chunk_size

    for chunk in get_chunks():
        try:
            screpo.insert_scrobbles_by_user(session, user_id, chunk)
            session.commit()
        except SQLAlchemyError:
            session.rollback()
            raise
        except Exception:
            raise


def get_max_timestamp(session: Session, user_id: int) -> datetime | None:
    return screpo.get_max_timestamp_by_user(session, user_id)
