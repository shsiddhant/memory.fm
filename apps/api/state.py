from __future__ import annotations
from memoryfm.models.sync_status import (
    EnsureUserStatus,
    SyncStatus,
)

sync_statuses: dict[str, SyncStatus] = {}
ensure_user_statuses: dict[str, EnsureUserStatus] = {}


def get_sync_status(username: str) -> SyncStatus:
    if username not in sync_statuses:
        sync_statuses[username] = SyncStatus()
    return sync_statuses[username]


def get_ensure_user_status(username: str) -> EnsureUserStatus:
    if username not in ensure_user_statuses:
        ensure_user_statuses[username] = EnsureUserStatus()
    return ensure_user_statuses[username]
