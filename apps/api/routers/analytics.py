from __future__ import annotations
from typing import Literal, Annotated
from fastapi import APIRouter, Query

from memoryfm.services.stats_service import get_top_charts_by_username

router = APIRouter()


@router.get("/user/{username}/top")
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
):
    return get_top_charts_by_username(username, kind, period, limit)
