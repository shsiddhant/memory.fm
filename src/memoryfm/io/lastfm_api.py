from __future__ import annotations
from typing import TYPE_CHECKING
import requests
import pandas as pd
import json
from memoryfm.errors import InvalidDataError
from memoryfm.io._normalise import normalise_lastfmstats

if TYPE_CHECKING:
    from collections.abc import Callable
    from typing import Any
    from memoryfm import ScrobbleLog


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


def df_from_recenttracks_response(response: requests.Response) -> pd.DataFrame:
    """
    Create a DataFrame from last.fm API method user.getRecentTracks response.

    Parameters
    ----------
    response : requests.Response
        A requests Response obtained from last.fm API method user.getRecentTracks

    Returns
    -------
    pd.DataFrame
        A pandas DataFrame of scrobbles, with columns - date, track, artist, album.
        Note date column contains timestamp as integer unix timestamp in seconds.

    """
    try:
        response.raise_for_status()
        jsondata = response.json()
    except requests.HTTPError as e:
        raise requests.HTTPError(json.loads(response.text), e.args)
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError from e
    else:
        if "recenttracks" not in jsondata.keys():
            raise InvalidDataError(f"Invalid Format:\n {jsondata}")
        elif "track" not in jsondata["recenttracks"].keys():
            raise InvalidDataError(f"Invalid Format:\n {jsondata}")
        else:
            data = jsondata["recenttracks"]["track"]
            if data:
                df = pd.json_normalize(jsondata["recenttracks"]["track"])
                required_cols = ["date.uts", "name", "artist.#text"]
                for col in required_cols:
                    if col not in df.columns:
                        return pd.DataFrame(
                            [], columns=["date", "track", "artist", "album"]
                        )
                if "album.#text" not in df.columns:
                    cols = required_cols
                else:
                    cols = required_cols
                    cols.append("album.#text")
                df = df[cols]
                df = df.rename(
                    columns={
                        "date.uts": "date",
                        "name": "track",
                        "artist.#text": "artist",
                        "album.#text": "album",
                    }
                )
                df["date"] = df["date"].astype(float)
                df = df.dropna(subset=["date", "track", "artist"])
                return df


def df_from_timestamp(
    username: str,
    api_key: str,
    timestamp: int | str | pd.Timestamp | None = None,
    limit: int = 180,
    statuscallback: Callable[..., Any] | None = None,
) -> pd.DataFrame:
    """
    Get DataFrame containing all scrobbles after a certain timestamp.
    Useful if you want recent scrobbles.

    Parameters
    ----------
    username : str
        A last.fm username.
    api_key : str
        A valid last.fm API key
    timestamp : int, str, pd.Timestamp, Optional
        An integer UNIX timestamp (in seconds), or a string represententing
        a valid datetime, or a pandas Timestamp.
        Only scrobbles since ``timestamp`` will be fetched.
    limit : int, default 180
        (Max 200) A rate limit for number of scrobbles per page.
    statuscallback : callable
        A callable to report status with callback. It is called on
        (page, totalpages, fetched_scrobbles, total_scrobbles, retry)

    Returns
    -------
    pd.DataFrame
        A pandas DataFrame of scrobbles, with columns - date, track, artist, album.
        Note date column contains timestamp as integer unix timestamp in seconds.

    """
    if timestamp is None:
        from_ts = None
    elif pd.api.types.is_number(timestamp):
        from_ts = int(pd.Timestamp(timestamp, unit="s").timestamp())
    else:
        from_ts = int(pd.Timestamp(timestamp, unit=None).timestamp())
    df = pd.DataFrame([], columns=["date", "track", "artist", "album"])
    df["date"] = df["date"].astype(int)
    page = 1
    totalpages = 1
    fetched_scrobbles = 0
    total_scrobbles = 0
    retry = 1
    while True:
        try:
            response = lastfm_get_recent_tracks(
                username,
                api_key,
                page=page,
                from_ts=from_ts,
                limit=limit,
            )
            df_page = df_from_recenttracks_response(response)
        except requests.HTTPError as e:
            if e.args[0]["error"] == 8 and retry <= 5:
                if statuscallback is not None:
                    statuscallback(
                        page, totalpages, fetched_scrobbles, total_scrobbles, retry
                    )
                retry = retry + 1
                continue
            else:
                raise
        else:
            if df_page is None or df_page.empty:
                if (df.empty or len(df) == 1) and statuscallback is not None:
                    statuscallback(0, 0, 0, 0)
                return df
            else:
                df = pd.concat([df, df_page], ignore_index=True)
                if statuscallback is not None:
                    total_scrobbles = int(
                        response.json()["recenttracks"]["@attr"]["total"]
                    )
                    fetched_scrobbles = len(df)
                    totalpages = int(
                        response.json()["recenttracks"]["@attr"]["totalPages"]
                    )
                    statuscallback(page, totalpages, fetched_scrobbles, total_scrobbles)
            retry = 0
            page += 1


def from_lastfm_api(
    username: str,
    api_key: str,
    tz: str | None = None,
    statuscallback: Callable[[int, int, int, int], Any] | None = None,
) -> ScrobbleLog:
    """
    Create ScrobbleLog from a last.fm username

    Parameters
    ----------
    username : str,
        A valid last.fm username.
    api_key : str,
        A valid last.fm API key.
    tz : str, Optional
        If not ``None``, ``tz`` must be a valid IANA Timezone string.
    statuscallback : callable
        A status callback to pass to df_from_timestamp to get status.

    Returns
    -------
    ScrobbleLog
        ScrobbleLog for the last.fm username.
    """
    df = df_from_timestamp(
        username,
        api_key,
        timestamp=None,
        statuscallback=statuscallback,
    )

    return normalise_lastfmstats(df, username, tz, unit="s", source="last.fm")
