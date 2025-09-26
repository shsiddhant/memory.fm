from pathlib import Path
import memoryfm as mfm
import pandas as pd
import pytest

data_dir  = Path(__file__).resolve().parent.parent / "data"
file = data_dir / "csv" / "sample.csv"
file_json = data_dir / "json" / "latest_scrobble.json"
sample_log = mfm.from_lastfmstats(file, "csv")
print(sample_log.meta)
data_valid = {  
                "timestamp": pd.Timestamp("2023-12-17 22:00"),
                "track": "Clementine",
                "artist": "Elliott Smith",
                "album": "Elliott Smith"
}

dict_valid = {
    "username": "sid",
    "scrobbles": [data_valid],
    "tz": "Asia/Kolkata"
}


dict_valid_2 = {
    "username": "sid",
    "scrobbles": [
        {
            "timestamp": pd.Timestamp("2023-12-05 20:00"),
            "track": "Tr1",
            "artist": "Ar1",
            "album": None
        }
    ],
    "tz": "Etc/UTC"
}

class TestScrobbleLog:
    def test_from_dict(self):
        scrobble_log = mfm.ScrobbleLog.from_dict(dict_valid)
        assert isinstance(scrobble_log, mfm.ScrobbleLog)
        assert scrobble_log.username == "sid"
        assert scrobble_log.df.iloc[0]["track"] == "Clementine"
        assert scrobble_log.tz == 'Asia/Kolkata'
        assert scrobble_log.meta["memory.fm_version"] == mfm.__version__

    def test_validate(self):
        dict_data = {
            "username": "sid",
            "scrobbles": [
                {"track": "Tr1",
                 "artist": "Ar1",
                 "album": None
                 }
            ],
            "tz": "Etc/UTC"
        }
        msg = "Required DataFrame column not found: timestamp"
        with pytest.raises(mfm.errors.SchemaError, match=msg):
            print(mfm.ScrobbleLog.from_dict(dict_data))
    
    def test_len(self):
        assert len(sample_log) == 13

    def test_slicing(self):
        assert sample_log[4].track == "Sad Girl"
        assert sample_log[5:7].df.iloc[1, 1] == "Starry Eyes"

    def test_eq(self):
        assert sample_log == sample_log[:]

    def test_contains(self):
        scrobble = sample_log[2]
        assert scrobble in sample_log

    def test_iter(self):
        for scrobble in sample_log:
            assert scrobble.artist in ("Lana Del Rey", "Cigarettes After Sex")

    def test_append(self):
        scrobble_log = mfm.ScrobbleLog.from_dict(dict_valid_2)
        assert len(scrobble_log) == 1
        scrobble = mfm.Scrobble.from_dict(data_valid)
        scrobble_log.append(scrobble)
        assert len(scrobble_log) == 2
        assert scrobble_log.df.iloc[0]["artist"] ==  "Ar1"
        assert scrobble_log.df.iloc[1]["album"] == "Elliott Smith"
        assert scrobble_log.tz == "Etc/UTC"

    def test_to_json(self, tmp_path):
        file_temp = tmp_path / "test_to_json.json"
        scrobble_log = mfm.from_lastfmstats(file_json, "json", tz="Europe/Berlin")
        scrobble_log.to_json(file_temp)
        content = file_temp.read_text()
        import json
        assert json.loads(content).get("meta")["source"] == "lastfmstats.com"
        assert json.loads(content).get("meta")["tz"] == "Europe/Berlin"
