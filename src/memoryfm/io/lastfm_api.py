from __future__ import annotations
from typing import Any
import requests
import json
import datetime
import logging
from zoneinfo import ZoneInfo

from memoryfm.errors import InvalidDataError
import memoryfm.services.user_service as userv
import memoryfm.services.scrobble_service as scserv

task_status: dict[str, Any] = {}

logging.basicConfig()
logger = logging.getLogger("sqlalchemy.engine")
logger.setLevel(logging.INFO)


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


def from_recenttracks_response(response: requests.Response) -> list[tuple]:
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
                scrobbles = [
                    (
                        int(s["date"]["uts"]),
                        s["name"],
                        s["artist"]["#text"],
                        s["album"]["#text"] if (s and "album" in s) else "",
                    )
                    for s in data
                ]
                return scrobbles
            else:
                return []


def from_timestamp(
    username: str,
    api_key: str,
    task_status: dict[str, Any],
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
    context = userv.get_user_context(username)
    user_id = None
    if context:
        user_id = context.get("user_id")
        tz = context.get("tz")
        userv.create_user(username, tz)
    if timestamp is None or isinstance(timestamp, int):
        from_ts = timestamp
    elif isinstance(timestamp, datetime.datetime):
        from_ts = int(timestamp.timestamp())
    else:
        raise ValueError("Invalid timestamp.")
    task_status["page"] = 1
    task_status["totalpages"] = 1
    task_status["fetched_scrobbles"] = 0
    task_status["total_scrobbles"] = 0
    task_status["retry"] = 1

    while True:
        try:
            response = lastfm_get_recent_tracks(
                username,
                api_key,
                page=task_status["page"],
                from_ts=from_ts,
                limit=limit,
            )
            data_page = from_recenttracks_response(response)
        except requests.HTTPError as e:
            if e.args[0]["error"] == 8 and task_status["retry"] <= 5:
                task_status["retry"] += 1
                continue
            else:
                raise
        else:
            if not data_page:
                task_status["status"] = "completed"
                logger.info(task_status)
                return
            elif user_id and tz:
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
                scserv.insert_scrobbles(user_id, batch, limit)
                task_status["total_scrobbles"] = int(
                    response.json()["recenttracks"]["@attr"]["total"]
                )
                task_status["fetched_scrobbles"] += len(batch)
                task_status["totalpages"] = int(
                    response.json()["recenttracks"]["@attr"]["totalPages"]
                )
                logger.info(task_status)
            task_status["retry"] = 0
            task_status["page"] += 1


def sync_lastfm_api(
    username: str,
    api_key: str,
    task_status: dict[str, Any],
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
    context = userv.get_user_context(username)
    user_id = context.get("user_id") if context else None
    if user_id:
        timestamp = scserv.get_max_timestamp(user_id)
    else:
        timestamp = None
    from_timestamp(username, api_key, task_status, timestamp, tz, limit)
