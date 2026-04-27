from __future__ import annotations
import datetime
from typing import TYPE_CHECKING

from memoryfm.models.service_enums import (
    ChartKindColumn,
)
import memoryfm.services.streaks_service as strkserv

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

kind = ChartKindColumn.Track
username = "lazulinoother"
year = 2024
min_length = 3
from_ts = datetime.datetime.fromtimestamp(1707419854)


def test_get_streaks_by_year(seeded_db: Session):
    streaks = strkserv.get_streaks_by_username(seeded_db, username, kind, from_ts)
    assert streaks is not None
    assert len(streaks) == 1, repr(streaks)
    for i, s in enumerate(streaks):
        print(i, repr(s))
    assert streaks[0][1].month == 2


def test_streaks_by_year(seeded_db: Session):
    streaks = strkserv.get_streaks_by_year(
        seeded_db,
        username,
        kind,
        year,
        min_length,
    )
    assert streaks is not None
    assert len(streaks) == 2
    assert streaks[0][2] == "Valentine"
    assert streaks[1][3] == 4
