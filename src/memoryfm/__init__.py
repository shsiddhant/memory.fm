"""Package: memoryfm"""

try:
    from importlib.metadata import version, PackageNotFoundError
except ImportError:
        from importlib_metadata import version, PackageNotFoundError
try:
    __version__ = version("memory.fm")
except PackageNotFoundError:
    __version__ = "0.0.0"    # Fallback value only

from memoryfm.core.objects import ScrobbleLog, Scrobble
from memoryfm.io.api import (
    from_lastfmstats,
    from_spotify,
    from_spotify_zip,
)

__all__ = [
    "from_lastfmstats",
    "from_spotify",
    "from_spotify_zip",
    "ScrobbleLog",
    "Scrobble",
]

