from __future__ import annotations
import os
import asyncio
from dotenv import load_dotenv
from typing import Literal, Annotated
from fastapi import (
    BackgroundTasks,
    FastAPI,
    Query,
    WebSocket,
    WebSocketDisconnect,
)
from memoryfm.db_services.stats import get_user_summary, get_top_charts
from memoryfm.io.lastfm_api import sync_lastfm_api, task_status

app = FastAPI()
load_dotenv()
API_KEY = os.getenv("API_KEY", "")


@app.post("/user/{username}/sync")
async def sync_scrobbles(username: str, bg_tasks: BackgroundTasks):
    task_status.clear()
    task_status["status"] = "running"
    bg_tasks.add_task(sync_lastfm_api, username, api_key=API_KEY)
    return {"message": f"Syncing scrobbles for user: {username}"}


@app.websocket("/ws/sync-progress")
async def sync_progress_websocket(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            await websocket.send_json(task_status)
            if task_status.get("status") == "completed":
                break
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        print("Client disconnected.")


@app.get("/user/{username}/summary")
def summary(username: str):
    return get_user_summary(username)


@app.get("/user/{username}/top={kind}")
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
):
    return get_top_charts(username, kind, period, limit)
