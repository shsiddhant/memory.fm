from __future__ import annotations
from typing import TYPE_CHECKING
from datetime import datetime
from zoneinfo import ZoneInfo

from memoryfm.errors import SchemaError, InvalidDataError
from memoryfm.io._loaders import load_json
from memoryfm.util.datetime_util import validate_tz
from memoryfm.db_services.basic_fetch import (
    create_user,
    get_userid_from_username,
    insert_scrobbles,
)

if TYPE_CHECKING:
    from pathlib import Path


def validate_lastfmstats(file: str | Path, tz: str | None = None):
    data = load_json(file)
    if not data:
        raise InvalidDataError("JSON data is empty")
    else:
        for key in ["username", "scrobbles"]:
            if key not in data.keys():
                raise SchemaError(f"Key missing in JSON file: '{key}'", key)
        username = data.get("username")
        scrobbles_data = data.get("scrobbles")
        tz = validate_tz(tz)
        return username, scrobbles_data, tz


def from_lastfmstats(file: str | Path, tz: str | None = None, overwrite: bool = False):
    username, scrobbles_data, tz = validate_lastfmstats(file, tz)
    if username and scrobbles_data:
        scrobbles = [
            {
                "timestamp": datetime.fromtimestamp(s["date"] / 1000, tz=ZoneInfo(tz)),
                "artist": s["artist"],
                "album": s["album"],
                "track": s["track"],
            }
            for s in scrobbles_data
        ]
        create_user(username, tz, overwrite)
        user_id = get_userid_from_username(username)
        if user_id:
            insert_scrobbles(user_id, scrobbles)
