from __future__ import annotations
from typing import Any
import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

task_status: dict[str, Any] = {}

router = APIRouter()


@router.websocket("/ws/sync-progress")
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
