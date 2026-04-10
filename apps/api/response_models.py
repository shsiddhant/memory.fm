from __future__ import annotations
from pydantic import BaseModel


class RecentScrobblesCount(BaseModel):
    day: str
    value: int
