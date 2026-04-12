from __future__ import annotations
from typing import TYPE_CHECKING
from memoryfm.io._loaders import load_json
from memoryfm.errors import SchemaError, InvalidDataError

if TYPE_CHECKING:
    from pathlib import Path


def validate_lastfmstats(file: str | Path):
    data = load_json(file)
    if not data:
        raise InvalidDataError("JSON data is empty")
    else:
        for key in ["username", "scrobbles"]:
            if key not in data.keys():
                raise SchemaError(f"Key missing in JSON file: '{key}'", key)
        username = data.get("username")
        scrobbles_data = data.get("scrobbles")
        return username, scrobbles_data
