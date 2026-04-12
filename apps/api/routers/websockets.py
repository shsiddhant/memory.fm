from __future__ import annotations
import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from memoryfm.models.sync_status import SyncStatus, SyncStatusTypes

sync_status: SyncStatus = SyncStatus()

router = APIRouter()


@router.websocket("/ws/sync-progress")
async def sync_progress_websocket(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            await websocket.send_json(sync_status.to_dict())
            if sync_status.status == SyncStatusTypes.Completed:
                break
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        print("Client disconnected.")
