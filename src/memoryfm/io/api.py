"""
Data IO API
"""

from memoryfm.io.lastfmstats import from_lastfmstats
from memoryfm.io.spotify import (
    from_spotify,
    from_spotify_zip,
)
from memoryfm.io.lastfm_api import from_lastfm_api

__all__ = [
    "from_lastfm_api",
    "from_lastfmstats",
    "from_spotify",
    "from_spotify_zip",
]
