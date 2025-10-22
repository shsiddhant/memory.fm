"""
Find version from Package metadata.
"""

try:
    from importlib.metadata import version, PackageNotFoundError
except ImportError:
    from importlib_metadata import version, PackageNotFoundError
try:
    __version__ = version("memory.fm")
except PackageNotFoundError:
    __version__ = "0.0.0"  # Fallback value only
