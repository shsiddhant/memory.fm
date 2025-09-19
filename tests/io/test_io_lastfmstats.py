import pytest
import pandas as pd
from pathlib import Path

from memoryfm.io._loaders import load_csv, load_json
from memoryfm.io.lastfmstats import from_lastfmstats, _validate_data
from memoryfm.io._normalise import normalise_lastfmstats
from memoryfm.errors import (
    ScrobbleError,
    SchemaError,
    ParseError,
    InvalidDataError
)

data_dir = Path(__file__).resolve().parent.parent / "data"
json_dir = data_dir / "json"
csv_dir = data_dir / "csv"
json_files_list = [
    "empty.json",
    "empty_json.json"
    "invalid_json.json"
    "sample.json"
    "wrong_column.json"
    "wrong_column_2.json"
]

class TestLoaders:
    def test_valid_json(self):
        expected_result = {"username":"lazulinoother",
                           "scrobbles":[
                               {"track":"Good Arms vs. Bad Arms",
                               "artist":"Frightened Rabbit",
                               "album":"The Midnight Organ Fight",
                               "albumId":"8bc361f4-0b80-35c9-8372-bb7c664d8d85",
                               "date":1757468274000},
                               {"track":"Floating in the Forth",
                                "artist":"Frightened Rabbit",
                                "album":"The Midnight Organ Fight",
                                "albumId":"8bc361f4-0b80-35c9-8372-bb7c664d8d85",
                                "date":1757514204000}]
                           }
        file = data_dir / "json" / "sample.json"
        data = load_json(file)
    
        assert data == expected_result
    
    def test_empty_file(self):
        msg = r".* at line 1 column 1"
        file = data_dir / "json" / "empty.json"
        with pytest.raises(ParseError, match=msg):
            return load_json(file)
    
    def test_valid_csv(self):
        file = csv_dir / "valid_data.csv"
        expected_result = {
                            "username": "lazulinoother",
                            "scrobbles":[
                                {"Artist": "LDR",
                                 "Album": "UV",
                                 "AlbumId": "a06",
                                 "Track": "Shades of Cool",
                                 "Date": 1594535082000
                                 }
                            ]
        }
        assert load_csv(file) == expected_result
    
    def test_mismatch_delimiter(self):
        file = csv_dir / "mismatch_delimiter.csv"
        msg = r"Expected delimiter ';' in line number 2: .*"
        with pytest.raises(InvalidDataError, match=msg):
            load_csv(file)
    
    def test_wrong_header_csv(self):
        file = csv_dir / "wrong_header.csv"
        msg = r"Expecting last column name: .*"
        with pytest.raises(InvalidDataError, match=msg):
            return load_csv(file)
    
    def test_no_username_csv(self):
        file = csv_dir / "no_username.csv"
        msg = "Blank or only whitespace username"
        with pytest.raises(InvalidDataError, match=msg):
            return load_csv(file)


class TestFromLastfmstats:
    def test_wrong_file_type(self):
        file = json_dir / "sample.json"
        msg = 'Only "json" or "csv" allowed as "file_type"'
        with pytest.raises(ScrobbleError, match=msg):
            from_lastfmstats(file, "jsom")

    def test_lastfmstats_validate_dict_type(self):
        data = []
        msg = "Expecting dict-like data"
        with pytest.raises(InvalidDataError, match=msg):
            _validate_data(data)

    def test_lastfmstats_validate_keys(self):
        data = {"Alpha": "user",
                "scrobbles": []
                }
        msg = "Key not found: 'username'"
        with pytest.raises(InvalidDataError, match=msg):
            _validate_data(data)

    def test_lastfmstats_validate_scrobble_type(self):
        data = {"username": "sid",
                "scrobbles": {"track", "name"}
                }
        msg = r"Expecting value of type 'list', 'dict', .*"
        with pytest.raises(InvalidDataError, match=msg):
            _validate_data(data)

    def test_lastfmstats_validata_username_type(self):
        data = {"username": {0},
                "scrobbles": []
                }
        msg = r"Expecting string type value .*"
        with pytest.raises(InvalidDataError, match=msg):
            _validate_data(data)

class TestNormaliseLastfmstats:

    def test_fromlastfmstats_normalise_no_date(self):
        df_data = {
                    "track" : ["tr1", "tr2"]
        }
        df = pd.DataFrame(df_data)
        with pytest.raises(SchemaError, match="Column not found"):
            normalise_lastfmstats(df=df, username="sid")

    def test_fromlastfmstats_normalise_bad_date(self):
        df_data = {
                    "date": ["2020-08-10", "dhj"]
        }
        df = pd.DataFrame(df_data)
<<<<<<< HEAD
        msg = r".* doesn't match format .*"
        with pytest.raises(SchemaError, match=msg):
            normalise_lastfmstats(df=df, username="sid")
=======
        msg = r"time data .* doesn't match format .*"
        with pytest.raises(SchemaError, match=msg):
            normalise_lastfmstats("sid", df, )
>>>>>>> 73eec99 (Added top  tracks/artists/albums charts, made all timestamps timezone aware and added a timezone attribute to object classes.)

    def test_fromlastfmstats_normalise(self):
        df_data = [
                    {
                        "track": "T1",
                        "artist": "Ar1",
                        "album": "Alb1",
                        "date": 1758122054033
                    }
        ]
        df = pd.DataFrame(df_data)
<<<<<<< HEAD
        dict_d = normalise_lastfmstats(
            username="sid", df=df, tz="Europe/London"
        ).to_dict(orient="records")
        assert dict_d["meta"]["tz"] == "Europe/London"
        assert dict_d["scrobbles"]
=======
        expected_dict = {"username": "sid",
                         "scrobbles": [
                             {
                                "timestamp":
                                 Timestamp(
                                    '2025-09-17 20:44:14.033000+0530',
                                     tz='Asia/Kolkata'
                                ),
                                "track": "T1",
                                "artist": "Ar1",
                                "album": "Alb1",
                             }
                         ],
                         "tzinfo": "Europe/London"
                         }
        dict_d = normalise_lastfmstats("sid", df, tz="Europe/London").to_dict(orient="records")
        assert dict_d == expected_dict
>>>>>>> 73eec99 (Added top  tracks/artists/albums charts, made all timestamps timezone aware and added a timezone attribute to object classes.)
