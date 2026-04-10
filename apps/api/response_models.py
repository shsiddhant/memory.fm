from __future__ import annotations
from pydantic import BaseModel
from datetime import date  # noqa: TC003


class ScrobblesCount(BaseModel):
    day: str
    value: int


class RecentActivity(BaseModel):
    from_date: date
    to_date: date
    counts: list[ScrobblesCount]
