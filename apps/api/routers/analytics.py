from __future__ import annotations
from typing import Literal, Annotated, Sequence
from fastapi import APIRouter, Depends, Query

from api.response_models import TopChart
from memoryfm.storage.session import get_db_session
import memoryfm.services.stats_service as stserv

router = APIRouter()


@router.get("/user/{username}/top", response_model=Sequence[TopChart] | None)
def top_charts(
    username: str,
    kind: Literal["artist", "album", "track"],
    period: Annotated[
        int | Literal["all_time"],
        Query(
            description="Filter by period of ```period``` days. "
            "**Set to all_time to view all time top charts.**"
        ),
    ] = 7,
    limit: Annotated[
        int,
        Query(
            description="The number of items to return. **Set to -1 to fetch all**",
            ge=-1,
            examples=[0, 10, 50],
        ),
    ] = 10,
    session=Depends(get_db_session),
):
    data = stserv.get_top_charts_by_username(session, username, kind, period, limit)
    return data
