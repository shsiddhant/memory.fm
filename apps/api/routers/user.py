from __future__ import annotations
import os
from dotenv import load_dotenv
from fastapi import APIRouter, BackgroundTasks
from .websockets import task_status
from memoryfm.io.lastfm_api import sync_lastfm_api
from memoryfm.services.stats_service import get_summary_by_username

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
    return get_summary_by_username(username)
