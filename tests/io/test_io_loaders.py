import pytest
from pathlib import Path

from memoryfm.io._loaders import load_json
from memoryfm.errors import ParseError


data_dir = Path(__file__).resolve().parent.parent / "data"
json_dir = data_dir / "json"


class TestLoaders:
    def test_valid_json(self):
        expected_result = {
            "username": "lazulinoother",
            "scrobbles": [
                {
                    "track": "Good Arms vs. Bad Arms",
                    "artist": "Frightened Rabbit",
                    "album": "The Midnight Organ Fight",
                    "albumId": "8bc361f4-0b80-35c9-8372-bb7c664d8d85",
                    "date": 1757468274000,
                },
                {
                    "track": "Floating in the Forth",
                    "artist": "Frightened Rabbit",
                    "album": "The Midnight Organ Fight",
                    "albumId": "8bc361f4-0b80-35c9-8372-bb7c664d8d85",
                    "date": 1757514204000,
                },
            ],
        }
        file = json_dir / "sample.json"
        data = load_json(file)

        assert data == expected_result

    def test_empty_file(self):
        msg = r".* at line 1 column 1"
        file = json_dir / "empty.json"
        with pytest.raises(ParseError, match=msg):
            return load_json(file)
