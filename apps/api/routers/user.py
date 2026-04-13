from __future__ import annotations
import os
from dotenv import load_dotenv
from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
)
from fastapi.exceptions import ResponseValidationError
from api.routers.websockets import sync_status
from api.response_models import (
    RecentActivity,
    SummaryModel,
)
from memoryfm.io.lastfm_api import sync_lastfm_api
from memoryfm.storage.session import get_db_session
import memoryfm.services.stats_service as stserv
from memoryfm.models.sync_status import SyncStatusTypes
from api.input_annotated_types import TrimmedStr  # noqa: TC001

router = APIRouter()

load_dotenv()
API_KEY = os.getenv("API_KEY", "")


@router.post("/user/{username}/sync")
async def sync_scrobbles(
    username: TrimmedStr,
    bg_tasks: BackgroundTasks,
    session=Depends(get_db_session),
):
    sync_status.clear()
    sync_status.status = SyncStatusTypes.Progress
    bg_tasks.add_task(
        sync_lastfm_api, session, username, api_key=API_KEY, sync_status=sync_status
    )
    return {"message": f"Syncing scrobbles for user: {username}"}


@router.get("/user/{username}/summary", response_model=SummaryModel)
def summary(username: TrimmedStr, session=Depends(get_db_session)):
    data = stserv.get_summary_by_username(session, username)
    if not data:
        raise ResponseValidationError(errors=[{"msg": "No data found for user."}])
    return data


@router.get("/user/{username}/recent_scrobbles", response_model=RecentActivity)
def recent_scrobbles(
    username: TrimmedStr,
    weeks: int = 8,
    session=Depends(get_db_session),
):
    data = stserv.get_daily_scrobbles_count(session, username, limit=weeks * 7)
    return RecentActivity.from_service_data(data)
