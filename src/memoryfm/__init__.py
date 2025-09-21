"""Package: memoryfm"""

try:
    from importlib.metadata import version, PackageNotFoundError
except ImportError:
        from importlib_metadata import version, PackageNotFoundError
try:
    __version__ = version("memory.fm")
except PackageNotFoundError:
    __version__ = "0.0.0.dev0"    # Fallback value only

from memoryfm.core.objects import ScrobbleLog, Scrobble
from memoryfm.io.api import from_lastfmstats

__all__ = [
        "from_lastfmstats",
        "ScrobbleLog",
        "Scrobble"
]

