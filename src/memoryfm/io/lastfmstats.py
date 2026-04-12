from __future__ import annotations
from typing import TYPE_CHECKING
from datetime import datetime
from zoneinfo import ZoneInfo

from memoryfm.util._validate import validate_lastfmstats
import memoryfm.services.user_service as userv
import memoryfm.services.scrobble_service as scserv

if TYPE_CHECKING:
    from pathlib import Path


def from_lastfmstats(file: str | Path, tz: str | None = None, overwrite: bool = False):
    username, scrobbles_data = validate_lastfmstats(file)
    if username and scrobbles_data:
        userv.create_user(username, tz, overwrite)
        context = userv.get_user_context(username)
        user_id = context.get("user_id") if context else None
        tz = context.get("tz") if context else tz
        if user_id and tz:
            scrobbles = [
                {
                    "timestamp": datetime.fromtimestamp(
                        s["date"] / 1000, tz=ZoneInfo(tz)
                    ),
                    "artist": s["artist"],
                    "album": s["album"],
                    "track": s["track"],
                }
                for s in scrobbles_data
            ]
            scserv.insert_scrobbles(user_id, scrobbles)
