"""Module models.py
Defines model classes:
ScrobbleLog : represents a scrobble log
Scrobble    : (dataclass) represents a single scrobble.
"""

from dataclasses import dataclass
import pandas as pd
from exceptions import ScrobbleError

@dataclass
class Scrobble:
    """Class representing a single scrobble."""
    timestamp: pd.Timestamp
    track: str
    artist: str
    album: str | None = None

    @classmethod
    def from_dict(cls, d):
        keys = ["timestamp", "track", "artist"]
        for key in keys:
            if key not in d.get(key):
                raise ScrobbleError(f"Missing {key}")
        
        return cls(timestamp=pd.Timestamp(d["timestamp"]), track=d["track"], artist=d["artist"], album=d["album"])


class ScrobbleLog:
    """Class representing a scrobble log."""
    def __init__(self, username, scrobbles_df):
        self.df = scrobbles_df
        self._validate_df()
    
    def _validate_df(self):

