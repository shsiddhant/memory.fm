from __future__ import annotations
import os
from typing import Annotated
from dotenv import load_dotenv
from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    Query,
)
from api.state.sync import run_sync, run_ensure_user
from api.response_models import (
    RecentActivity,
    SummaryModel,
)
from memoryfm.storage.session import get_db_session
import memoryfm.services.stats_service as stserv
from api.input_annotated_types import TrimmedStr  # noqa: TC001

router = APIRouter()

load_dotenv()
API_KEY = os.getenv("API_KEY", "")


@router.post("/user/{username}/ensure")
async def ensure_user(
    username: TrimmedStr,
    bg_tasks: BackgroundTasks,
    session=Depends(get_db_session),
):
    """Ensure that user with username exist. If not, create one."""
    bg_tasks.add_task(run_ensure_user, session, username)
    return {"status": "accepted", "message": f"Ensure user task started for {username}"}


@router.post("/user/{username}/sync")
async def sync_scrobbles(
    username: TrimmedStr,
    bg_tasks: BackgroundTasks,
    session=Depends(get_db_session),
):
    """Sync scrobbles for user from last.fm API."""
    bg_tasks.add_task(
        run_sync,
        session,
        username,
        api_key=API_KEY,
    )
    return {"status": "accepted", "message": f"Sync task started for {username}"}


@router.get("/user/{username}/summary", response_model=SummaryModel | None)
def summary(username: TrimmedStr, session=Depends(get_db_session)):
    """Get summary stats for user."""
    return stserv.get_summary_by_username(session, username)


@router.get("/user/{username}/recent_scrobbles", response_model=RecentActivity)
def recent_scrobbles(
    username: TrimmedStr,
    weeks: Annotated[int, Query(description="Number of weeks to fetch ", ge=1)] = 8,
    session=Depends(get_db_session),
):
    """Get recent daily scrobble counts for user."""
    data = stserv.get_daily_scrobbles_count(session, username, limit=weeks * 7)
    return RecentActivity.from_service_data(data)
