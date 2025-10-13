import pytest
import pandas as pd
# from pathlib import Path

from memoryfm.errors import SchemaError
# from memoryfm.io.spotify import (
#     from_spotify,
#     from_spotify_zip,
# )
from memoryfm.io._normalise import normalise_spotify


class TestFromSpotify:

    def test_normalise_spotify_missing_column(self):
        data = {
            "ts":["2024-05-05", "greenbutterfly"],
            #"ms_played":[250000, 17120],
            "master_metadata_track_name": ["a", "b"],
            "master_metadata_album_album_name": ["c", "d"],
            "master_metadata_album_artist_name": ["e", "f"]
        }
        msg = r"Missing expected column:.*"
        with pytest.raises(SchemaError, match=msg):
            normalise_spotify(df=pd.DataFrame(data), username="vartika")

    def test_normalise_spotify_wrong_type(self):
        data = {
            "ts":["2024-05-05", "greenbutterfly"],
            "ms_played":[250000, "themonster"],
            "master_metadata_track_name": ["a", "b"],
            "master_metadata_album_album_name": ["c", "d"],
            "master_metadata_album_artist_name": ["e", "f"],
            'reason_end': ["trackdone", "endplay"],
        }
        msg = r"Column expected to contain only numeric values*"
        with pytest.raises(SchemaError, match=msg):
            normalise_spotify(df=pd.DataFrame(data))

