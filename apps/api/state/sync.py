from __future__ import annotations
from typing import TYPE_CHECKING
import asyncio

from api.state.status_services import get_sync_status, get_ensure_user_status
from api.state.locks import get_lock
from memoryfm.io.lastfm_api import sync_lastfm_api
from memoryfm.services.user_service import ensure_user

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


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


async def run_ensure_user(session: Session, username: str):
    ensure_sync_status = get_ensure_user_status(username)
    lock = get_lock(username)

    async with lock:
        await asyncio.to_thread(
            ensure_user,
            session,
            username,
            ensure_sync_status,
        )
