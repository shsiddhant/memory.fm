from __future__ import annotations
import os
from dotenv import load_dotenv
from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
)
from fastapi.responses import JSONResponse
from api.routers.websockets import task_status
from api.response_models import RecentActivity, ScrobblesCount
from memoryfm.io.lastfm_api import sync_lastfm_api
from memoryfm.storage.db import get_db_session
import memoryfm.services.stats_service as stserv
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
    task_status.clear()
    task_status["status"] = "running"
    bg_tasks.add_task(
        sync_lastfm_api, session, username, api_key=API_KEY, task_status=task_status
    )
    return {"message": f"Syncing scrobbles for user: {username}"}


@router.get("/user/{username}/summary")
def summary(username: TrimmedStr, session=Depends(get_db_session)):
    return stserv.get_summary_by_username(session, username)


@router.get("/user/{username}/recent_scrobbles", response_model=RecentActivity)
def recent_scrobbles(
    username: TrimmedStr,
    weeks: int = 8,
    session=Depends(get_db_session),
):
    data = stserv.get_daily_scrobbles_count(session, username, limit=weeks * 7)
    if data is not None:
        from_date, to_date, counts_seq = data
        counts = [
            ScrobblesCount(day=row["Date"].strftime("%Y-%m-%d"), value=row["Scrobbles"])
            for row in counts_seq
        ]
        return RecentActivity(from_date=from_date, to_date=to_date, counts=counts)
    return JSONResponse(status_code=404, content={"message": "No data found."})
