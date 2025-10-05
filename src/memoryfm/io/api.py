"""
Data IO api
"""

from memoryfm.io.lastfmstats import from_lastfmstats
from memoryfm.io.spotify import from_spotify

__all__ = ["from_lastfmstats", "from_spotify"]
