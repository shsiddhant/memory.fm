from __future__ import annotations
from typing import TYPE_CHECKING
import requests
import json
import logging
import datetime
from zoneinfo import ZoneInfo

from memoryfm.errors import InvalidDataError, UserNotFoundError
from memoryfm.models.sync_status import SyncStatusTypes
from memoryfm.util.format_sync_log import format_status_log
from memoryfm.models.service_helpers import parse_lastfm_api_response
import memoryfm.services.user_service as userv
import memoryfm.services.scrobble_service as scserv

if TYPE_CHECKING:
    from sqlalchemy.orm import Session
    from memoryfm.models.sync_status import SyncStatus

logger = logging.getLogger(__name__)


def lastfm_get_recent_tracks(
    username: str,
    api_key: str,
    page: int = 1,
    from_ts: int | None = None,
    to_ts: int | None = None,
    limit: int = 180,
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
    limit : int, default 180
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
    response = requests.get(url)
    return response


def from_recenttracks_response(
    response: requests.Response,
) -> tuple[list[tuple[int, str, str, str]], list[str], int] | None:
    """
    Get data from last.fm API method user.getRecentTracks response.

    Parameters
    ----------
    response : requests.Response
        A requests Response obtained from last.fm API method user.getRecentTracks

    Returns
    -------
    list[tuple]
        A list of scrobble dicts, with keys - date, track, artist, album.
        Note date column contains timestamp as integer unix timestamp in seconds.

    """
    try:
        response.raise_for_status()
        jsondata = response.json()
    except requests.HTTPError as e:
        raise requests.HTTPError(json.loads(response.text), e.args)
    except json.JSONDecodeError:
        raise
    else:
        if "recenttracks" not in jsondata.keys():
            raise InvalidDataError(f"Invalid Format:\n {jsondata}")
        elif "track" not in jsondata["recenttracks"].keys():
            raise InvalidDataError(f"Invalid Format:\n {jsondata}")
        else:
            data = jsondata["recenttracks"]["track"]
            if data:
                return parse_lastfm_api_response(data)
            else:
                return None


def from_timestamp(
    session: Session,
    username: str,
    api_key: str,
    sync_status: SyncStatus,
    timestamp: int | datetime.datetime | None = None,
    tz: str | None = "Etc/UTC",
    limit: int = 180,
):
    """
    Fetch and insert all scrobbles after a certain timestamp.
    Useful if you want recent scrobbles for incremental sync.

    Parameters
    ----------
    username : str
        A last.fm username.
    api_key : str
        A valid last.fm API key
    timestamp : int, str, datetime.datetime, Optional
        An integer UNIX timestamp (in seconds), or a string represententing
        a valid datetime, or a datetime object.
        Only scrobbles since ``timestamp`` will be fetched.
    tz : str, Optional
        If not ``None``, ``tz`` must be a valid IANA Timezone string.
    limit : int, default 180
        (Max 200) A rate limit for number of scrobbles per page.

    """
    context = None
    try:
        userv.create_user(session, username, tz)
        context = userv.get_user_context(session, username)
    except UserNotFoundError as e:
        logger.warning("User not found: %s", e.username)
        raise
    except Exception:
        raise
    user_id, tz = context.user_id, context.tz
    if timestamp is None or isinstance(timestamp, int | float):
        from_ts = int(timestamp) if timestamp else timestamp
    elif isinstance(timestamp, datetime.datetime):
        from_ts = int(timestamp.timestamp())
    else:
        raise ValueError("Invalid timestamp.")
    sync_status.page = 1
    sync_status.totalpages = 1
    sync_status.fetched_scrobbles = 0
    sync_status.total_scrobbles = 0
    sync_status.retry = 1
    sync_status.total_retries = 5
    skipped_count = 0
    page_block = 20

    while True:
        _, modpage = divmod(sync_status.page, page_block)
        # Write progress or skips every 20 pages.
        if modpage == 0:
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
        try:
            response = lastfm_get_recent_tracks(
                username,
                api_key,
                page=sync_status.page,
                from_ts=from_ts,
                limit=limit,
            )
            data = from_recenttracks_response(response)
            if not data:
                if sync_status.page > sync_status.totalpages:
                    sync_status.page -= 1
                sync_status.status = SyncStatusTypes.Completed
                logger.info(format_status_log(username, sync_status))
                return
            elif user_id and tz:
                data_page, _, skipped_count_page = data
                skipped_count += skipped_count_page
                batch = [
                    {
                        "timestamp": datetime.datetime.fromtimestamp(
                            int(s[0]), tz=ZoneInfo(tz)
                        ),
                        "track": s[1],
                        "artist": s[2],
                        "album": s[3],
                    }
                    for s in data_page
                ]
                scserv.insert_scrobbles(session, user_id, batch, limit)
                sync_status.total_scrobbles = int(
                    response.json()["recenttracks"]["@attr"]["total"]
                )
                sync_status.fetched_scrobbles += len(batch)
                sync_status.totalpages = int(
                    response.json()["recenttracks"]["@attr"]["totalPages"]
                )
        except requests.HTTPError as e:
            if (
                e.args[0]["error"] == 8
                and sync_status.retry <= sync_status.total_retries
            ):
                sync_status.retry += 1
                sync_status.status = SyncStatusTypes.Retry
                logger.info(format_status_log(username, sync_status))
                continue
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
    limit: int = 180,
):
    """
    Fetch and sync scrobbles from a last.fm username using last.fm API.

    Parameters
    ----------
    username : str,
        A valid last.fm username.
    api_key : str,
        A valid last.fm API key.
    tz : str, Optional
        If not ``None``, ``tz`` must be a valid IANA Timezone string.

    """
    try:
        context = userv.get_user_context(session, username)
        timestamp = scserv.get_max_timestamp(session, context.user_id)
    except UserNotFoundError:
        timestamp = None
    except Exception as e:
        logger.error(e)
        raise
    sync_status.status = SyncStatusTypes.Started
    logger.info(format_status_log(username, sync_status))
    from_timestamp(session, username, api_key, sync_status, timestamp, tz, limit)
