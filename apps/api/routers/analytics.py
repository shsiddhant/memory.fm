from __future__ import annotations
from typing import Literal, Annotated, Sequence
from fastapi import APIRouter, Depends, Query

from api.response_models import TopChart
from memoryfm.models.service_enums import ChartKindColumn  # noqa: TC001
from memoryfm.storage.session import get_db_session
import memoryfm.services.stats_service as stserv

router = APIRouter()


@router.get("/user/{username}/top_last", response_model=Sequence[TopChart] | None)
def top_charts_recent(
    username: str,
    kind: Annotated[ChartKindColumn, Query(description="Type of top chart to fetch.")],
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
            description="The number of items to return. **Set to -1 to fetch all.**",
            ge=-1,
            examples=[0, 10, 50],
        ),
    ] = 10,
    session=Depends(get_db_session),
):
    """Fetch top charts by period."""
    data = stserv.get_top_charts_by_period(session, username, kind, period, limit)
    return data
