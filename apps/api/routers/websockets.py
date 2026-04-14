from __future__ import annotations
from dataclasses import asdict
import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from memoryfm.models.sync_status import (
    SyncStatusTypes,
    UserExist,
)

from api.state.status_services import get_ensure_user_status, get_sync_status

router = APIRouter()


@router.websocket("/ws/sync-progress")
async def sync_progress_websocket(websocket: WebSocket):
    await websocket.accept()
    username = websocket.query_params.get("username")
    if not username:
        await websocket.close(1008)
        return

    try:
        while True:
            sync_status = get_sync_status(username)
            await websocket.send_json(sync_status.to_dict())
            if sync_status.status == SyncStatusTypes.Completed:
                break
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        pass


@router.websocket("/ws/ensure-user")
async def ensure_user_websocket(websocket: WebSocket):
    await websocket.accept()
    username = websocket.query_params.get("username")
    if not username:
        await websocket.close(1008)
        return
    ensure_user_status = get_ensure_user_status(username)
    try:
        while True:
            await websocket.send_json(asdict(ensure_user_status))
            if ensure_user_status.status == UserExist.Exists:
                break
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        pass
