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

"""

from __future__ import annotations
import pandas as pd
from typing import TYPE_CHECKING

from memoryfm.errors import InvalidDataError
from memoryfm.io._loaders import load_csv, load_json
from memoryfm.io._normalise import normalise_lastfmstats

if TYPE_CHECKING:
    from typing import (
        IO,
        Literal,
    )
    from memoryfm._typing import PathLike
    from memoryfm.core.objects import ScrobbleLog


def from_lastfmstats(
    file: PathLike | IO[str], file_type: Literal["json", "csv"], tz: str | None = None
) -> ScrobbleLog:
    """
    Create a ScrobbleLog from a JSON/CSV export obtained from
    `lastfmstats <https://lastfmstats.com>`_.

    Parameters
    ----------
    file : PathLike or TextIOBase object.
        * A pathlib path, or
        * A string corresponding to a path, such as
          ``/home/username/Documents/filename``, or
        * A TextIOBase object having a ``read()`` method.
    file_type : Literal["json", "csv"]
       The type of file must either be 'json' or 'csv'.
    tz : str, default None
        IANA Timezone string.

        If not passed, attempt to use
        ``tzlocal.get_localzone_name`` to calculate it. If ``tzlocal`` is not found,
        default to 'Etc/UTC'.

    Returns
    -------
    ScrobbeLog

    """
    if file_type == "json":
        data = load_json(file)
    elif file_type == "csv":
        data = load_csv(file)
    else:
        raise InvalidDataError('Only "json" or "csv" allowed as "file_type"')
    _validate_data(data)
    username = data["username"]
    df = pd.DataFrame(data["scrobbles"])
    scrobble_log = normalise_lastfmstats(df, username, tz)
    return scrobble_log


def _validate_data(data: dict) -> None:
    """
    Validate data types and dictionary keys.
    """
    if not hasattr(data, "keys"):
        raise InvalidDataError("Expecting dict type data")
    for key in ["username", "scrobbles"]:
        if key not in data.keys():
            raise InvalidDataError(f"Key not found: '{key}'")
    if not isinstance(data["scrobbles"], (list, dict, pd.DataFrame)):
        raise InvalidDataError(
            "Expecting value of type "
            "'list', 'dict', or 'pandas.DataFrame' for key: scrobbles"
        )
    if not isinstance(data["username"], str):
        raise InvalidDataError("Expecting string type value for key: username")
