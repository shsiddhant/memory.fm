import pytest
from pathlib import Path
from sqlalchemy import select
from sqlalchemy.orm import Session
from memoryfm.util._validate import validate_lastfmstats
from memoryfm.errors import (
    SchemaError,
    InvalidDataError,
)
import memoryfm.services.user_service as userv
from memoryfm.models.core import Scrobble

data_dir = Path(__file__).resolve().parent.parent / "data"
json_dir = data_dir / "json"
csv_dir = data_dir / "csv"
file = json_dir / "sample.json"


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

    def test_from_lastfmstats(self, seeded_db: Session):
        context = userv.get_user_context(seeded_db, username="lazulinoother")
        assert context.tz == "Asia/Kolkata"
        user_id = context.user_id

        stmt = select(Scrobble).where(Scrobble.user_id == user_id)
        scrobbles = seeded_db.execute(stmt).fetchall()
        assert len(scrobbles) == 11
