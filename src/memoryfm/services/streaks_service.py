import datetime
from zoneinfo import ZoneInfo

from sqlalchemy.orm import Session

from memoryfm.models.service_enums import ChartKindColumn
import memoryfm.storage.streaks as strkrepo
from memoryfm.storage.user_repo import get_user_by_username


def get_streaks_by_username(
    session: Session,
    username: str,
    kind: ChartKindColumn,
    from_ts: datetime.datetime | None = None,
    to_ts: datetime.datetime | None = None,
    min_length: int = 2,
):
    user = get_user_by_username(session, username)
    if user:
        user_id = user.id
        return strkrepo.get_streaks(
            session,
            user_id,
            kind,
            from_ts,
            to_ts,
            min_length,
        )
    return None


def get_streaks_by_year(
    session: Session,
    username: str,
    kind: ChartKindColumn,
    year: int,
    min_length: int = 2,
    tz: str = "Etc/UTC",
):
    from_ts = datetime.datetime(year=year, month=1, day=1, tzinfo=ZoneInfo(tz))
    to_ts = datetime.datetime(year=year, month=12, day=31, tzinfo=ZoneInfo(tz))
    return get_streaks_by_username(
        session,
        username,
        kind,
        from_ts,
        to_ts,
        min_length,
    )
