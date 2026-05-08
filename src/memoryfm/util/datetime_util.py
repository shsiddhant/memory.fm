from __future__ import annotations
import datetime
from typing import Literal
import logging
from zoneinfo import ZoneInfo
from tzlocal import get_localzone_name

from memoryfm.errors import InvalidDataError


logger = logging.getLogger(__name__)


def validate_tz(tz: str | None = None) -> str:
    """Set timezone value from valid IANA string.

    If no value or `None` passed, tries to use tzlocal to
    get the timezone value.
    Fallback: Etc/UTC
    """
    if tz is not None:
        from zoneinfo import ZoneInfo, ZoneInfoNotFoundError  # noqa: PLC0415

        try:
            ZoneInfo(tz)
            return tz
        except (ZoneInfoNotFoundError, IsADirectoryError, TypeError) as e:
            raise InvalidDataError("Invalid IANA timezone string") from e
    else:
        try:
            return get_localzone_name()
        except Exception as e:
            logger.error("Error: %s.\nUsing Etc/UTC as fallback.", e)
            return "Etc/UTC"


def get_datelimit_from_period(period: int | Literal["all_time"] = 7):
    if period != "all_time":
        return datetime.datetime.now(tz=ZoneInfo("Etc/UTC")) - datetime.timedelta(
            days=period
        )
    else:
        return datetime.datetime.fromtimestamp(0, tz=ZoneInfo("Etc/UTC"))


def normalize_timestamp(
    timestamp: datetime.datetime | None, tz: str = "Etc/UTC"
) -> datetime.datetime | None:
    if not timestamp:
        return None
    if timestamp.tzinfo is None:
        return timestamp.replace(tzinfo=ZoneInfo(tz))
    return timestamp.astimezone(tz=ZoneInfo(tz))
