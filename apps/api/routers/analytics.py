import datetime
from typing import Literal, Annotated, Sequence
from fastapi import APIRouter, Depends, Query

from api.response_models import TopChart
from memoryfm.models.service_enums import ChartKindColumn
from memoryfm.services.user_service import get_user_context
from memoryfm.storage.session import get_db_session
import memoryfm.services.stats_service as stserv
from memoryfm.util.datetime_util import normalize_timestamp

router = APIRouter()


@router.get("/user/{username}/top_last", response_model=Sequence[TopChart])
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
        int | None,
        Query(
            description="The number of items to return.",
            gt=0,
            examples=[0, 10, 50],
        ),
    ] = 10,
    session=Depends(get_db_session),
):
    """Fetch top charts by period."""
    return stserv.get_top_charts_by_period(session, username, kind, period, limit) or []


@router.get("/user/{username}/top", response_model=Sequence[TopChart])
def top_charts(
    username: str,
    kind: Annotated[ChartKindColumn, Query(description="Type of top chart to fetch.")],
    from_ts: Annotated[
        datetime.datetime | None,
        Query(description="Fetch top charts since this date. *Use ISO 8601 datetime.*"),
    ] = None,
    to_ts: Annotated[
        datetime.datetime | None,
        Query(description="Fetch top charts upto this date. *Use ISO 8601 datetime.*"),
    ] = None,
    limit: Annotated[
        int | None,
        Query(
            description="The number of items to return.",
            gt=0,
            examples=[0, 10, 50],
        ),
    ] = 10,
    session=Depends(get_db_session),
):
    """Fetch top charts by period."""
    tz = get_user_context(session, username).tz
    return (
        stserv.get_top_charts_by_username(
            session,
            username,
            kind,
            from_ts=normalize_timestamp(from_ts, tz),
            to_ts=normalize_timestamp(to_ts, tz),
            limit=limit,
        )
        or []
    )
