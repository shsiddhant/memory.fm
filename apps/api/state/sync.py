from __future__ import annotations
import logging
from typing import TYPE_CHECKING
import asyncio

from fastapi.responses import JSONResponse

from apps.api.state.status_services import get_sync_status, get_ensure_user_status
from apps.api.state.locks import get_lock
from memoryfm.io.lastfm_api import sync_lastfm_api, refresh_scrobbles_lastfm_api
from memoryfm.models.sync_status import (
    EnsureUserStatus,
    SyncStatus,
    SyncStatusTypes,
    UserExist,
)
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


def apply_exception_to_ensure_status(
    e: Exception, ensure_user_status: EnsureUserStatus
):
    ensure_user_status.status = UserExist.Checking

    if isinstance(
        e,
        (
            err.LastfmAPIError,
            err.APIKeyError,
            err.RateLimitExceededError,
        ),
    ):
        ensure_user_status.error = e.msg
    else:
        ensure_user_status.error = str(e)


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


async def run_ensure_user(session: Session, username: str, api_key: str):
    ensure_sync_status = get_ensure_user_status(username)
    lock = get_lock(username)

    async with lock:
        ensure_sync_status.error = None
        try:
            userinfo = await asyncio.to_thread(
                ensure_user,
                session,
                username,
                api_key,
                ensure_sync_status,
            )
            return userinfo
        except Exception as e:
            logger.error(str(e))
            if isinstance(
                e,
                (
                    err.LastfmAPIError,
                    err.APIKeyError,
                    err.RateLimitExceededError,
                ),
            ):
                ensure_sync_status.error = e.msg
                errors = [{"code": e.code, "msg": e.msg}]

            elif isinstance(e, err.UserNotFoundError):
                ensure_sync_status.error = str(e)
                errors = [{"code": 6, "msg": str(e)}]
            else:
                errors = [{"code": 31, "msg": str(e)}]
            return JSONResponse(status_code=422, content={"errors": errors})


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
