from __future__ import annotations
from dataclasses import asdict, dataclass, fields
from enum import Enum


class SyncPhase(Enum):
    Backfill = "backfill"
    Recent = "recent"


class SyncStatusTypes(Enum):
    Started = 1
    Progress = 2
    Completed = 3
    Retry = 4
    Error = 5
    Warning = 6


@dataclass
class SyncStatus:
    status: SyncStatusTypes | None = None
    page: int | None = None
    totalpages: int | None = None
    fetched_scrobbles: int | None = None
    total_scrobbles: int | None = None
    retry: int | None = None
    total_retries: int | None = None
    error: str | None = None
    phase: SyncPhase | None = None

    def clear(self):
        for field in fields(self):
            setattr(self, field.name, None)

    def to_dict(self):
        return asdict(self)


class UserExist(Enum):
    Exists = 1
    Checking = 2
    Error = 3


@dataclass
class EnsureUserStatus:
    status: UserExist | None = None
