from __future__ import annotations
import os
from dotenv import load_dotenv
from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
)
from fastapi.exceptions import ResponseValidationError
from api.state.status_services import get_ensure_user_status, get_sync_status
from api.state.sync import run_sync
from api.response_models import (
    RecentActivity,
    SummaryModel,
)
from memoryfm.storage.session import get_db_session
import memoryfm.services.stats_service as stserv
import memoryfm.services.user_service as userv
from memoryfm.models.sync_status import SyncStatusTypes
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
    ensure_user_status = get_ensure_user_status(username)
    bg_tasks.add_task(userv.ensure_user, session, username, ensure_user_status)
    return {"msg": f"Ensuring user exists: {username}..."}


@router.post("/user/{username}/sync")
async def sync_scrobbles(
    username: TrimmedStr,
    bg_tasks: BackgroundTasks,
    session=Depends(get_db_session),
):
    sync_status = get_sync_status(username)
    sync_status.clear()
    sync_status.status = SyncStatusTypes.Progress
    bg_tasks.add_task(
        run_sync,
        session,
        username,
        api_key=API_KEY,
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
