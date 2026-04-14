from __future__ import annotations
from typing import TYPE_CHECKING
import asyncio

from api.state.status_services import get_sync_status
from memoryfm.io.lastfm_api import sync_lastfm_api

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

user_locks: dict[str, asyncio.Lock] = {}


def get_lock(username: str):
    if username not in user_locks:
        user_locks[username] = asyncio.Lock()
    return user_locks[username]


async def run_sync(session: Session, username: str, api_key: str):
    sync_status = get_sync_status(username)
    lock = get_lock(username)

    async with lock:
        await asyncio.to_thread(
            sync_lastfm_api,
            session,
            username,
            api_key,
            sync_status,
        )
