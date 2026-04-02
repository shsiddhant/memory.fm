from __future__ import annotations
import logging
from tzlocal import get_localzone_name

from memoryfm.errors import InvalidDataError

logging.basicConfig(level=logging.ERROR)


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
            logging.error("Error: %s.\nUsing Etc/UTC as fallback.", e)
            return "Etc/UTC"
