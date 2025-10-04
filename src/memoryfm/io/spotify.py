"""Module: memoryfm.io.spotify
Read Spotify Listening History exports and return a ScrobbleLog
"""

from __future__ import annotations
import pandas as pd
from typing import TYPE_CHECKING

from memoryfm._typing import PathLike
from memoryfm.errors import InvalidDataError
from memoryfm.io._loaders import load_json
from memoryfm.core.objects import ScrobbleLog
from memoryfm.io._normalise import normalise_spotify

if TYPE_CHECKING:
    from typing import (
        IO,
        AnyStr,
    )

def from_spotify(
    file: PathLike | IO[AnyStr],
    username: str | None = None,
    tz: str | None = None
) -> ScrobbleLog:
    """Create a ScrobbleLog from Spotify export.
    """
    data = load_json(file)
    df = pd.DataFrame(data)
    scrobble_log = normalise_spotify(df)
    return scrobble_log
