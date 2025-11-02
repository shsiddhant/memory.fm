from __future__ import annotations
from pathlib import Path
import pandas as pd
from memoryfm.stats.streaks import streaks, gen_streak_bool
import memoryfm as mfm


json_file = Path(__file__).resolve().parent.parent / "data/json/canonical_json.json"
sclog = mfm.ScrobbleLog.from_json(json_file)


class TestStreaks:
    def test_get_streak_bool(self):
        series = pd.Series([1, 2, 2, 2, 4, 5, 5])
        assert all(gen_streak_bool(series) == [0, 1, 1, 0, 0, 1])

    def test_streaks(self):
        assert streaks(sclog, "artist", minlength=2).loc[0, "length"] == 4
        assert streaks(sclog, "artist", minlength=2).loc[0, "artist"] == "Lana Del Rey"
