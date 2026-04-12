from __future__ import annotations
from typing import Literal, Annotated
from fastapi import APIRouter, Depends, Query

from api.service_deps import get_stats_service

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
    stserv=Depends(get_stats_service),
):
    return stserv.get_top_charts_by_username(username, kind, period, limit)
