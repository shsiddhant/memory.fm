"""Module: memoryfm.io.lastfmstats

Read data obtained from parsing lastfmstats.com exports (json/csv),
check neccesary column properties ('username', 'scrobbles'),
and extract the nested data from scrobbles column as a DataFrame.

Example of a valid lastfmstats-username.json (optional column "albumId")
------------------------------------------------------------------------------
{"username":"lazulinoother", "scrobbles":[{"track":"They'll Only Miss
You When You Leave","artist":"Carissa's Wierd","album":"Songs About Leaving",
"albumId":"948a8a4c-23f3-4bf2-b201-dcb68a89b897","date":1757352413000}]}
------------------------------------------------------------------------------

Corresponding DataFrame base_df obtained using utils.loaders.parse_json

Functions: verify_columns,
           extract_scrobble_dataframe,
           verify_scrobbles_columns
"""
from __future__ import annotations
import pandas as pd
from typing import TYPE_CHECKING

from memoryfm._typing import PathLike
from memoryfm.errors import InvalidDataError, ScrobbleError
from memoryfm.io._loaders import load_csv, load_json
from memoryfm.io._normalise import normalise_lastfmstats
from memoryfm.core.objects import ScrobbleLog

if TYPE_CHECKING:
    from typing import IO, AnyStr, Literal


def from_lastfmstats(
    file: PathLike | IO[AnyStr],
    file_type: Literal["json", "csv"],
    tz: str | None = None
) ->ScrobbleLog:
    """
    """
    if file_type == "json":
        data = load_json(file)
    elif file_type == "csv":
        data = load_csv(file)
    else:
        raise ScrobbleError('Only "json" or "csv" allowed as "file_type"')
    _validate_data(data) 
    username = data["username"]
    df = pd.DataFrame(data["scrobbles"])
    scrobble_log = normalise_lastfmstats(df, username, tz)
    return scrobble_log


def _validate_data(data: dict) -> None:
    """

    """
    if not hasattr(data, "keys"):
        raise InvalidDataError("Expecting dict-like data")
    for key in ['username', 'scrobbles']:
        if key not in data.keys():
            raise InvalidDataError(f"Key not found: '{key}'")
    if not isinstance(data['scrobbles'], (list, dict, pd.DataFrame)):
        raise InvalidDataError(
            "Expecting value of type "
            "'list', 'dict', or 'pandas.DataFrame' for key 'scrobbles'"
        )
    if not isinstance(data['username'], str):
            raise InvalidDataError("Expecting string type value for key 'username'")
