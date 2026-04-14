from __future__ import annotations
from dataclasses import asdict, dataclass, fields
from enum import Enum


class SyncPhase(Enum):
    Backfill = "backfill"
    Recent = "recent"


class SyncStatusTypes(Enum):
    Started = "started"
    Progress = "progress"
    Completed = "completed"
    Retry = "retry"
    Error = "error"
    Warning = "warning"


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
        return serialize(asdict(self))


class UserExist(Enum):
    Exists = "exists"
    Checking = "checking"
    Error = "error"


@dataclass
class EnsureUserStatus:
    status: UserExist | None = None

    def to_dict(self):
        return serialize(asdict(self))


def serialize(obj):
    if isinstance(obj, Enum):
        return obj.value
    if isinstance(obj, dict):
        return {k: serialize(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [serialize(v) for v in obj]

    return obj
