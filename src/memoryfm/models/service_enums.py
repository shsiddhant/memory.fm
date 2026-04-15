from __future__ import annotations
from enum import Enum
from memoryfm.models.core import Scrobble


class ChartKindColumn(Enum):
    Artist = "artist"
    Album = "album"
    Track = "track"

    @property
    def column(self):
        mapping = {
            "artist": Scrobble.artist,
            "album": Scrobble.album,
            "track": Scrobble.track,
        }
        return mapping[self.value]


class Frequency(Enum):
    D = "day"
    W = "week"
    M = "month"
    Q = "quarter"
    Y = "year"
