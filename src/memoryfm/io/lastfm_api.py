from __future__ import annotations
from pathlib import Path
from typing import TYPE_CHECKING
import requests
import json
import logging
import datetime
from zoneinfo import ZoneInfo

from sqlalchemy.exc import SQLAlchemyError

from memoryfm.config import DEBUG_DIR
from memoryfm.errors import (
    APIKeyError,
    InvalidDataError,
    RateLimitExceededError,
    UserLoginRequiredError,
    UserNotFoundError,
    LastfmAPIError,
)
from memoryfm.models.sync_status import SyncPhase, SyncStatusTypes
from memoryfm.util.format_sync_log import format_status_log
from memoryfm.models.service_helpers import parse_lastfm_api_response
import memoryfm.services.user_service as userv
import memoryfm.services.scrobble_service as scserv

from pydantic import ValidationError

if TYPE_CHECKING:
    from sqlalchemy.orm import Session
    from memoryfm.models.sync_status import SyncStatus
    from memoryfm.models.service_helpers import LastfmResponse

logger = logging.getLogger(__name__)


def lastfm_get_recent_tracks(
    username: str,
    api_key: str,
    page: int = 1,
    from_ts: int | None = None,
    to_ts: int | None = None,
    limit: int = 200,
) -> requests.Response:
    """
    Fetch response from last.fm API method user.getRecentTracks.

    Parameters
    ----------
    username : str
        A last.fm username.
    api_key : str
        A valid last.fm API key
    page : int, default 1
        Page number to fetch.
    from_ts : int, Optional
        A UNIX timestamp (in seconds). Only scrobbles since ``from_ts`` will be fetched.
    to_ts : int, Optional
        A UNIX timestamp (in seconds). Only scrobbles upto ``to_ts`` will be fetched.
    limit : int, default 200
        (Max 200) A rate limit for number of scrobbles per page.

    Returns
    -------
    Response
        A requests Response for the API call.

    """
    url = (
        f"http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks"
        f"&user={username}&api_key={api_key}&page={page}&from={from_ts}&to={to_ts}"
        f"&limit={limit}&format=json"
    )
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
        "Accept-Encoding": "identity",  # Forces raw, uncompressed 8-bit data
    }
    response = requests.get(url, headers=headers)
    return response


def from_recenttracks_response(
    response: requests.Response,
) -> LastfmResponse:
    """
    Get data from last.fm API method user.getRecentTracks response.

    Parameters
    ----------
    response : requests.Response
        A requests Response obtained from last.fm API method user.getRecentTracks

    Returns
    -------
    LastfmResponse
        A custom pydantic model for valid last.fm API response

    """
    try:
        response_data = response.json()
        return parse_lastfm_api_response(response_data)
    except json.JSONDecodeError:
        if DEBUG_DIR:
            with open(Path(DEBUG_DIR) / "failed-lastfm-response.txt", "w") as fp:
                fp.write(response.text)
            with open(Path(DEBUG_DIR) / "failed-lastfm-response.bin", "wb") as fp:
                fp.write(response.content)
            print("URL", response.url)
        raise
    except InvalidDataError:
        raise
    except ValidationError:
        raise


def fetch_by_timestamps(
    session: Session,
    username: str,
    api_key: str,
    sync_status: SyncStatus,
    from_ts: int | None = None,
    to_ts: int | None = None,
    tz: str | None = "Etc/UTC",
    limit: int = 200,
):
    """
    Fetch and insert all scrobbles between two timestamps.
    Useful if you want incremental sync.

    Parameters
    ----------
    session: Session
        An sqlalchemy Session
    username : str
        A last.fm username.
    api_key : str
        A valid last.fm API key
    sync_status : SyncStatus
        A SyncStatus object to store progress and status.
        This is used to log the progress.
    from_ts : int, Optional
        A UNIX timestamp (in seconds). Only scrobbles since ``from_ts`` will be fetched.
    to_ts : int, Optional
        A UNIX timestamp (in seconds). Only scrobbles upto ``to_ts`` will be fetched.
    tz : str, Optional
        If not ``None``, ``tz`` must be a valid IANA Timezone string.
    limit : int, default 200
        (Max 200) A rate limit for number of scrobbles per page.
    """
    sync_status.page = 1
    sync_status.totalpages = 1
    sync_status.fetched_scrobbles = 0
    sync_status.total_scrobbles = 0
    sync_status.retry = 1
    sync_status.total_retries = 5
    skipped_count = 0
    page_block = 10

    try:
        userv.create_user(session, username, tz)
        context = userv.get_user_context(session, username)
    except UserNotFoundError as e:
        logger.warning("User not found: %s", e.username)
        raise
    except Exception:
        raise
    user_id, tz = context.user_id, context.tz

    while True:
        # Break loop if page exceeds total pages
        if sync_status.page > sync_status.totalpages:
            sync_status.page -= 1
            sync_status.status = SyncStatusTypes.Completed
            logger.info(format_status_log(username, sync_status))
            break

        # Write progress after every `page_block` pages.
        _, modpage = divmod(sync_status.page, page_block)
        if modpage == 0 or sync_status.page == 1:
            # If skipped scrobbles, write warning to log
            if skipped_count > 0:
                sync_status.status = SyncStatusTypes.Warning
                text = "scrobbles" if skipped_count > 1 else "scrobble"
                skipped_text = f"Skipping {skipped_count} {text} - missing timestamps."
                sync_status.error = skipped_text if skipped_count > 0 else None
                logger.warning(format_status_log(username, sync_status))

            # Write progress to log
            sync_status.status = SyncStatusTypes.Progress
            logger.info(format_status_log(username, sync_status))

        # Fetch scrobbles from last.fm API
        try:
            response = lastfm_get_recent_tracks(
                username, api_key, sync_status.page, from_ts, to_ts, limit
            )
            valid_response = from_recenttracks_response(response)
            batch = [
                {
                    "timestamp": datetime.datetime.fromtimestamp(
                        s.timestamp, tz=ZoneInfo(tz)
                    ),
                    "track": s.track,
                    "artist": s.artist,
                    "album": s.album,
                }
                for s in valid_response.scrobbles
            ]
            if not batch:
                sync_status.status = SyncStatusTypes.Completed
                logger.info(format_status_log(username, sync_status))
                break
            sync_status.status = SyncStatusTypes.Progress
            scserv.insert_scrobbles(session, user_id, batch)
            sync_status.totalpages = valid_response.totalpages
            sync_status.total_scrobbles = valid_response.total_scrobbles
            sync_status.fetched_scrobbles += len(batch)
        except LastfmAPIError as e:
            if e.code in (8, 11) and sync_status.retry <= sync_status.total_retries:
                sync_status.retry += 1
                sync_status.status = SyncStatusTypes.Retry
                logger.info(format_status_log(username, sync_status))
                continue
            elif e.code == 6:
                raise UserNotFoundError(username)
            elif e.code == 17:
                raise UserLoginRequiredError(e.msg)
            elif e.code in (10, 26):
                raise APIKeyError(e.code, e.msg)
            elif e.code == 29:
                raise RateLimitExceededError(e.msg)
            else:
                raise
        else:
            sync_status.retry = 0
            sync_status.page += 1


def sync_lastfm_api(
    session: Session,
    username: str,
    api_key: str,
    sync_status: SyncStatus,
    tz: str | None = None,
    limit: int = 1000,
):
    """
    Fetch and sync scrobbles from a last.fm username using last.fm API.

    Parameters
    ----------
    session: Session,
        An SQLAlchemy Session
    username : str,
        A valid last.fm username.
    api_key : str,
        A valid last.fm API key.
    sync_status : SyncStatus
        A SyncStatus object to store progress and status.
        This is used to log the progress.
    tz : str, Optional
        If not ``None``, ``tz`` must be a valid IANA Timezone string.
    limit : int, default 200
        (Max 200) A rate limit for number of scrobbles per page.

    """
    first_ts, last_ts = None, None
    try:
        context = userv.get_user_context(session, username)
        timestamps = scserv.get_end_timestamps(session, context.user_id)
        if timestamps:
            first_dt, last_dt = timestamps
            first_ts = int(first_dt.timestamp()) if first_dt else None
            last_ts = int(last_dt.timestamp()) if last_dt else None
    except UserNotFoundError:
        first_ts, last_ts = None, None
    except Exception as e:
        logger.error(e)
        raise
    sync_status.status = SyncStatusTypes.Started
    logger.info(format_status_log(username, sync_status))

    # Backfill if old missing scrobbles
    if first_ts:
        sync_status.phase = SyncPhase.Backfill
        fetch_by_timestamps(
            session,
            username,
            api_key,
            sync_status,
            from_ts=None,
            to_ts=first_ts,
            tz=tz,
            limit=limit,
        )
    # Insert recent scrobbles
    sync_status.phase = SyncPhase.Recent
    fetch_by_timestamps(
        session,
        username,
        api_key,
        sync_status,
        from_ts=last_ts,
        to_ts=None,
        tz=tz,
        limit=limit,
    )


def refresh_scrobbles_lastfm_api(
    session: Session,
    username: str,
    api_key: str,
    sync_status: SyncStatus,
    limit: int = 1000,
):
    try:
        context = userv.get_user_context(session, username)
        if context:
            user_id = context.user_id
            tz = context.tz
            logger.info("[REFRESHING SCROBBLES] | %s", username)
            logger.info("[DELETING SCROBBLES] | %s", username)
            scserv.delete_scrobbles(session, user_id)
            logger.info("[DELETED SCROBBLES] | %s", username)
            sync_lastfm_api(session, username, api_key, sync_status, tz, limit)
    except SQLAlchemyError as e:
        session.rollback()
        logger.error(e)
