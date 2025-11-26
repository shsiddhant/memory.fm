from __future__ import annotations
from typing import TYPE_CHECKING
import requests
import pandas as pd
import json
from memoryfm.errors import InvalidDataError
from memoryfm.io._normalise import normalise_lastfmstats

if TYPE_CHECKING:
    from memoryfm import ScrobbleLog


def lastfm_get_recent_tracks(
    username: str,
    api_key: str,
    page: int = 1,
    from_ts: int | None = None,
    to_ts: int | None = None,
    limit: int = 180,
) -> dict:
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
        Note date column contains timestamp as unix timestamp in seconds.
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
                df = pd.json_normalize(jsondata["recenttracks"]["track"])[
                    [
                        "date.uts",
                        "name",
                        "artist.#text",
                        "album.#text",
                    ]
                ]
                df = df.rename(
                    columns={
                        "date.uts": "date",
                        "name": "track",
                        "artist.#text": "artist",
                        "album.#text": "album",
                    }
                )
                df["date"] = df["date"].astype(int)
                return df


def df_from_timestamp(
    username: str,
    api_key: str,
    timestamp: int | str | pd.Timestamp,
    limit: int = 180,
) -> pd.DataFrame:
    """
    Get DataFrame containing scrobbles after a certain timestamp.
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
    retry = 5
    while True and retry > 0:
        try:
            df_page = df_from_recenttracks_response(
                lastfm_get_recent_tracks(
                    username,
                    api_key,
                    page=page,
                    from_ts=from_ts,
                    limit=limit,
                )
            )
        except requests.HTTPError as e:
            if e.args[0]["error"] == 8:
                retry = retry - 1
                continue
            else:
                raise requests.HTTPError from e
        else:
            if df_page is None or df_page.empty:
                return df
            else:
                df = pd.concat([df, df_page], ignore_index=True)
            retry = 5
            page += 1


def from_lastfm_api(
    username: str,
    api_key: str,
    tz: str | None = None,
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
    Returns
    -------
    ScrobbleLog
        ScrobbleLog for the last.fm username.
    """
    df = df_from_timestamp(username, api_key, timestamp=None)
    return normalise_lastfmstats(df, username, tz, unit="s")
