import datetime
from typing import Literal, Annotated, Sequence
from fastapi import APIRouter, Depends, Query

from api.response_models import AttachmentMoment, TimeSeriesData, TopChart
from memoryfm.models.service_enums import ChartKindColumn, Frequency
from memoryfm.services.user_service import get_user_context
from memoryfm.storage.session import get_db_session
import memoryfm.services.stats_service as stserv
import memoryfm.services.attachment_service as attserv
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
        Query(
            description="Fetch top charts since this datetime. *Use ISO 8601 datetime.*"
        ),
    ] = None,
    to_ts: Annotated[
        datetime.datetime | None,
        Query(
            description="Fetch top charts upto this datetime. *Use ISO 8601 datetime.*"
        ),
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
    """Fetch top charts for user in the given datetime range."""
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


@router.get("/user/{username}/attachment", response_model=Sequence[TimeSeriesData])
def attachment_index(
    username: str,
    kind: Annotated[
        ChartKindColumn, Query(description="Kind of Attachment Index to fetch.")
    ],
    from_ts: Annotated[
        datetime.datetime | None,
        Query(
            description=(
                "Fetch attachment index since this datetime. *Use ISO 8601 datetime.*"
            )
        ),
    ] = None,
    to_ts: Annotated[
        datetime.datetime | None,
        Query(
            description=(
                "Fetch attachment index upto this datetime. *Use ISO 8601 datetime.*"
            )
        ),
    ] = None,
    freq: Annotated[
        Frequency,
        Query(
            description="The Frequency over which scrobble counts are grouped together."
        ),
    ] = Frequency.D,
    alpha: Annotated[
        float,
        Query(
            description=(
                "Order of Attachment Index. "
                "The order is same as order of the underlying Rényi Entropy."
            ),
            ge=0.5,
            le=3.0,
        ),
    ] = 1,
    session=Depends(get_db_session),
):
    """Fetch Attachment Index for user in the given datetime range."""
    tz = get_user_context(session, username).tz
    return (
        attserv.get_attachment_index_by_username(
            session,
            username,
            kind,
            normalize_timestamp(from_ts, tz),
            normalize_timestamp(to_ts, tz),
            freq,
            alpha,
        )
        or []
    )


@router.get(
    "/user/{username}/attachment_moments", response_model=Sequence[AttachmentMoment]
)
def attachment_moments(
    username: str,
    kind: Annotated[
        ChartKindColumn, Query(description="Kind of Attachment Moments to fetch.")
    ],
    from_ts: Annotated[
        datetime.datetime | None,
        Query(
            description=(
                "Fetch attachment moments since this datetime. *Use ISO 8601 datetime.*"
            )
        ),
    ] = None,
    to_ts: Annotated[
        datetime.datetime | None,
        Query(
            description=(
                "Fetch attachment moments upto this datetime. *Use ISO 8601 datetime.*"
            )
        ),
    ] = None,
    freq: Annotated[
        Frequency,
        Query(
            description="The Frequency over which scrobble counts are grouped together."
        ),
    ] = Frequency.D,
    alpha: Annotated[
        float,
        Query(
            description=(
                "Order of Attachment Index to use for attachment moments. "
                "The order is same as order of the underlying Rényi Entropy."
            ),
            ge=0.5,
            le=3.0,
        ),
    ] = 1,
    threshold: Annotated[
        float,
        Query(
            description="Threshold z_score for choosing top attachment moments.", ge=1
        ),
    ] = 1,
    session=Depends(get_db_session),
):
    """Fetch Attachment Moments for user in the given datetime range."""
    tz = get_user_context(session, username).tz
    return (
        attserv.get_attachment_moments(
            session,
            username,
            kind,
            normalize_timestamp(from_ts, tz),
            normalize_timestamp(to_ts, tz),
            freq,
            alpha,
            threshold,
        )
        or []
    )


@router.get(
    "/user/{username}/attachment_moments_last",
    response_model=Sequence[AttachmentMoment],
)
def attachment_moments_last(
    username: str,
    kind: Annotated[
        ChartKindColumn, Query(description="Kind of Attachment Moments to fetch.")
    ],
    period: Annotated[
        int | Literal["all_time"],
        Query(
            description="Filter by period of ```period``` days. "
            "**Set to all_time to fetch all time moments.**"
        ),
    ] = 90,
    freq: Annotated[
        Frequency,
        Query(
            description="The Frequency over which scrobble counts are grouped together."
        ),
    ] = Frequency.D,
    alpha: Annotated[
        float,
        Query(
            description=(
                "Order of Attachment Index to use for attachment moments. "
                "The order is same as order of the underlying Rényi Entropy."
            ),
            ge=0.5,
            le=3.0,
        ),
    ] = 1,
    threshold: Annotated[
        float,
        Query(
            description="Threshold z_score for choosing top attachment moments.", ge=1
        ),
    ] = 1,
    session=Depends(get_db_session),
):
    """Fetch Attachment Moments for user in the given period."""
    return (
        attserv.get_attachment_moments_by_period(
            session,
            username,
            kind,
            period,
            freq,
            alpha,
            threshold,
        )
        or []
    )
