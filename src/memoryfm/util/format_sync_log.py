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
    phaseinfo = f"[{sync_status.phase.name.upper()}]" if sync_status.phase else ""
    commoninfo = f"{phaseinfo} | {userinfo} | {pageinfo}"

    if sync_status.status == SyncStatusTypes.Started:
        text = f"[SYNC STARTED] {phaseinfo} | {userinfo}"
    elif sync_status.status == SyncStatusTypes.Progress:
        text = f"[SYNC PROGRESS] {commoninfo} | {scrobbleinfo}"
    elif sync_status.status == SyncStatusTypes.Completed:
        text = f"[SYNC COMPLETED] {commoninfo} | {scrobbleinfo}"
    elif sync_status.status == SyncStatusTypes.Retry:
        text = f"[SYNC RETRY] {commoninfo} | {retryinfo}"
    elif sync_status.status == SyncStatusTypes.Error:
        text = f"[SYNC ERROR] {commoninfo} | {sync_status.error}"
    elif sync_status.status == SyncStatusTypes.Warning and sync_status.error:
        text = f"[SYNC Warning] {commoninfo} | {sync_status.error}"
    else:
        raise ValueError("Invalid sync_status.status")
    return text
