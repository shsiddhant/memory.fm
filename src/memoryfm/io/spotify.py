"""Module: memoryfm.io.spotify
Read Spotify listening history exports and return a ScrobbleLog
"""

from __future__ import annotations
import pandas as pd
import zipfile
import io
from typing import TYPE_CHECKING

from memoryfm._typing import PathLike
from memoryfm.io._loaders import load_json
from memoryfm.core.objects import ScrobbleLog
from memoryfm.io._normalise import normalise_spotify

if TYPE_CHECKING:
    from typing import (
        IO,
        AnyStr,
    )


def from_spotify_zip(
    file: PathLike | IO[AnyStr],
    username: str | None = None,
    tz: str | None = None,
    min_duration_ms: int | None = 60000,
) -> list[str]:
    """
    Create a ScrobbleLog from a Spotify listening history zip.

    Parameters
    ---------- 
    file : PathLike or TextIOBase object.
        * A pathlib path, or
        * A string corresponding to a path, such as
          ``/home/username/Documents/filename``, or
        * A TextIOBase object having a ``read()`` method.

        The file is expected to be a Spotify listening history zip file.
    username : str, default None
        A string representing username. Spotify export exports may not include the
        username. If no username is passed, then it will be set to None.
    tz : str, default None
        IANA Timezone string.
        
        If not passed, attempt to use
        ``tzlocal.get_localzone_name`` to calculate it. If ``tzlocal`` is not found,
        default to 'Etc/UTC'.
    min_duration_ms : int, default 60000
        An integer representing the minimum duration played in milliseconds. Any
        listen with duration less than ``min_duration_ms`` shall be discarded and
        not included in the ScrobbleLog. Set to 60000 (1 minute) by default.

    Returns
    -------
    ScrobbleLog

    """
    scrobble_logs_list = []
    with zipfile.ZipFile(file) as spotify_zip:
        json_file_list = [f.filename for f in spotify_zip.filelist if (
            f.filename.endswith('.json') and
            f.filename.count('Streaming_History_Audio')
        )]
        for name in json_file_list:
            with spotify_zip.open(name) as json_file:
                scrobble_logs_list.append(
                    from_spotify(
                        io.TextIOWrapper(json_file, encoding='UTF-8'),
                        username,
                        tz,
                        min_duration_ms
                    )
                )
    scrobble_log, *others = scrobble_logs_list
    for log in others:
        scrobble_log.append(log)

    return scrobble_log

 
def from_spotify(
    file: PathLike | IO[AnyStr],
    username: str | None = None,
    tz: str | None = None,
    min_duration_ms: int | None = 60000,
) -> ScrobbleLog:
    """
    Create a ScrobbleLog from a Spotify export JSON.

    Parameters
    ---------- 
    file : PathLike or TextIOBase object.
        * A pathlib path, or
        * A string corresponding to a path, such as
          ``/home/username/Documents/filename``, or
        * A TextIOBase object having a ``read()`` method.

        The file is expected to be a Spotify listening history JSON.
    username : str, default None
        A string representing username. Spotify export exports may not include the
        username. If no username is passed, then it will be set to None.
    tz : str, default None
        IANA Timezone string.
        
        If not passed, attempt to use
        ``tzlocal.get_localzone_name`` to calculate it. If ``tzlocal`` is not found,
        default to 'Etc/UTC'.
    min_duration_ms : int, default 60000
        An integer representing the minimum duration played in milliseconds. Any
        listen with duration less than ``min_duration_ms`` shall be discarded and
        not included in the ScrobbleLog. Set to 60000 (1 minute) by default.

    Returns
    -------
    ScrobbleLog

    """
    data = load_json(file)
    df = pd.DataFrame(data)
    scrobble_log = normalise_spotify(df=df, username=username, tz=tz,
                                      min_duration_ms=min_duration_ms)
    return scrobble_log
