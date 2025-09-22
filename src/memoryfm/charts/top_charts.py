from __future__ import annotations
import pandas as pd
#from typing import TYPE_CHECKING

from memoryfm import ScrobbleLog

def top_charts_markdown(
    scrobble_log: ScrobbleLog,
    kind: str = "track",
    n: int = 5
) ->pd.Series:
    """
    Get top `n` tracks/artists/albums by number of scrobbles.
    """ 
    kind = kind.lower().strip().rstrip("s")
    kind_print_dict = {
        "track": "Tracks",
        "artist": "Artists",
        "album": "Albums"
    }
    count_series = scrobble_log.top_charts(kind, n)
    top_charts_markdown = count_series.to_markdown()
    return {
        "kind_print": kind_print_dict.get(kind),
        "markdown": top_charts_markdown
    }
