"""
Find version from Package metadata.
"""

import sys

if sys.version_info >= (3, 8):
    from importlib.metadata import PackageNotFoundError, version
else:
    from importlib_metadata import PackageNotFoundError, version
try:
    __version__ = version("memory.fm")
except PackageNotFoundError:
    __version__ = "0.0.0"  # Fallback value only
