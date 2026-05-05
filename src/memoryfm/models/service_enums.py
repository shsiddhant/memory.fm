from enum import Enum
from sqlalchemy.orm import InstrumentedAttribute

from memoryfm.models.core import AnalyticsView, Scrobble


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

    @property
    def id_column(self) -> InstrumentedAttribute[int]:
        mapping = {
            "artist": AnalyticsView.artist_id,
            "album": AnalyticsView.album_id,
            "track": AnalyticsView.track_id,
        }
        return mapping[self.value]

    @property
    def name_column(self) -> InstrumentedAttribute[str]:
        mapping = {
            "artist": AnalyticsView.artist,
            "album": AnalyticsView.album,
            "track": AnalyticsView.track,
        }
        return mapping[self.value]

    @property
    def subname_column(self) -> InstrumentedAttribute[str] | None:
        mapping: dict[str, InstrumentedAttribute[str] | None] = {
            "artist": None,
            "album": AnalyticsView.artist,
            "track": AnalyticsView.artist,
        }
        return mapping[self.value]


class Frequency(Enum):
    D = "day"
    W = "week"
    M = "month"
    Q = "quarter"
    Y = "year"
