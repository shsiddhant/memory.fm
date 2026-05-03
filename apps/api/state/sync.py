from __future__ import annotations
import logging
from typing import TYPE_CHECKING
import asyncio

from apps.api.state.status_services import get_sync_status, get_ensure_user_status
from apps.api.state.locks import get_lock
from memoryfm.io.lastfm_api import sync_lastfm_api, refresh_scrobbles_lastfm_api
from memoryfm.models.sync_status import SyncStatus, SyncStatusTypes
from memoryfm.services.user_service import ensure_user
from memoryfm.util.format_sync_log import format_status_log
import memoryfm.errors as err

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

logger = logging.getLogger("memoryfm.io.lastfm_api")


def apply_exception_to_status(e: Exception, sync_status: SyncStatus):
    sync_status.status = SyncStatusTypes.Error

    if isinstance(
        e,
        (
            err.LastfmAPIError,
            err.UserLoginRequiredError,
            err.APIKeyError,
            err.RateLimitExceededError,
        ),
    ):
        sync_status.error = e.msg
    else:
        sync_status.error = str(e)


async def run_sync(session: Session, username: str, api_key: str):
    sync_status = get_sync_status(username)
    lock = get_lock(username)

    async with lock:
        sync_status.error = None
        try:
            await asyncio.to_thread(
                sync_lastfm_api,
                session,
                username,
                api_key,
                sync_status,
            )
        except Exception as e:
            apply_exception_to_status(e, sync_status)
            logger.error(format_status_log(username, sync_status))


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


async def run_refresh(session: Session, username: str, api_key: str):
    sync_status = get_sync_status(username)
    lock = get_lock(username)

    async with lock:
        sync_status.error = None
        try:
            await asyncio.to_thread(
                refresh_scrobbles_lastfm_api,
                session,
                username,
                api_key,
                sync_status,
            )
        except Exception as e:
            apply_exception_to_status(e, sync_status)
            logger.error(format_status_log(username, sync_status))
