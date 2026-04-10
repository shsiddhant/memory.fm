from __future__ import annotations
from collections.abc import Sequence
import os
from dotenv import load_dotenv
from fastapi import APIRouter, BackgroundTasks
from fastapi.responses import JSONResponse
from .websockets import task_status
from api.response_models import RecentScrobblesCount
from memoryfm.io.lastfm_api import sync_lastfm_api
import memoryfm.services.stats_service as stserv

router = APIRouter()

load_dotenv()
API_KEY = os.getenv("API_KEY", "")


@router.post("/user/{username}/sync")
async def sync_scrobbles(username: str, bg_tasks: BackgroundTasks):
    task_status.clear()
    task_status["status"] = "running"
    bg_tasks.add_task(
        sync_lastfm_api, username, api_key=API_KEY, task_status=task_status
    )
    return {"message": f"Syncing scrobbles for user: {username}"}


@router.get("/user/{username}/summary")
def summary(username: str):
    return stserv.get_summary_by_username(username)


@router.get(
    "/user/{username}/recent_scrobbles", response_model=Sequence[RecentScrobblesCount]
)
def recent_scrobbles(username: str, weeks: int = 8):
    data = stserv.get_daily_scrobbles_count(username, limit=weeks * 7)
    if data is not None:
        return [
            RecentScrobblesCount(day=row["Date"], value=row["Scrobbles"])
            for row in data
        ]
    return JSONResponse(status_code=404, content={"message": "No data found."})
