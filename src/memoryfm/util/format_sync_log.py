from __future__ import annotations
from memoryfm.models.sync_status import SyncStatusTypes, SyncStatus


def format_status_log(
    username: str,
    sync_status: SyncStatus,
):
    userinfo = f"user={username}"
    pageinfo = f"page={sync_status.page}/{sync_status.totalpages}"
    scrobbleinfo = (
        f"fetched={sync_status.fetched_scrobbles}/{sync_status.total_scrobbles}"
    )
    retryinfo = f"attempt={sync_status.retry}/{sync_status.total_retries}"
    if sync_status.status == SyncStatusTypes.Started:
        text = f"[SYNC STARTED] {userinfo}"
    elif sync_status.status == SyncStatusTypes.Progress:
        text = f"[SYNC PROGRESS] {userinfo} | {pageinfo} | {scrobbleinfo}"
    elif sync_status.status == SyncStatusTypes.Completed:
        text = f"[SYNC COMPLETED] {userinfo} | {pageinfo} | {scrobbleinfo}"
    elif sync_status.status == SyncStatusTypes.Retry:
        text = f"[SYNC RETRY] {userinfo} | {pageinfo} | {retryinfo}"
    elif sync_status.status == SyncStatusTypes.Error:
        text = f"[SYNC ERROR] {userinfo} | {pageinfo} | {sync_status.error}"
    else:
        raise ValueError("Invalid sync_status.status")
    return text
