"""Module: memoryfm.io.spotify
Read Spotify Listening History exports and return a ScrobbleLog
"""

from __future__ import annotations
import pandas as pd
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

def from_spotify(
    file: PathLike | IO[AnyStr],
    username: str | None = None,
    tz: str | None = None,
    min_duration_ms: int | None = 60000,
) -> ScrobbleLog:
    """Create a ScrobbleLog from Spotify export.
    """
    data = load_json(file)
    df = pd.DataFrame(data)
    scrobble_log = normalise_spotify(df=df, username=username, tz=tz,
                                     min_duration_ms=min_duration_ms)
    return scrobble_log
