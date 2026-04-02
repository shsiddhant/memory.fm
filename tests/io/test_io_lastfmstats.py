import pytest
from pathlib import Path

from memoryfm.io.lastfmstats import validate_lastfmstats, from_lastfmstats
from memoryfm.errors import (
    SchemaError,
    InvalidDataError,
)

data_dir = Path(__file__).resolve().parent.parent / "data"
json_dir = data_dir / "json"
csv_dir = data_dir / "csv"


class TestFromLastfmstats:
    def test_validate_lastfmstats_empty_data(self):
        file = json_dir / "empty_json.json"
        msg = "JSON data is empty"
        with pytest.raises(InvalidDataError, match=msg):
            validate_lastfmstats(file)

    def test_validate_lastfmstats_missing_key(self):
        file = json_dir / "wrong_key.json"
        msg = "Key missing in JSON file: 'username'"
        with pytest.raises(SchemaError, match=msg):
            validate_lastfmstats(file)

    def test_lastfmstats_wrong_scrobble_type(self):
        file = json_dir / "wrong_scrobbles_type.json"
        with pytest.raises(TypeError):
            from_lastfmstats(file)
