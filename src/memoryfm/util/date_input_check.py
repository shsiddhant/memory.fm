from __future__ import annotations
from typing import TYPE_CHECKING
import pandas as pd
from memoryfm.errors import (
    InvalidDataError,
    InvalidTypeError,
)

if TYPE_CHECKING:
    import datetime


def validate_tz(tz: str | None = None) -> str:
    """Set timezone value from valid IANA string.

    If no value or `None` passed, tries to use tzlocal to
    get the timezone value.
    Fallback: Etc/UTC
    """
    if not isinstance(tz, str | None):
        raise InvalidTypeError("Expecting string type value for tz")
    elif tz is not None:
        from zoneinfo import ZoneInfo, ZoneInfoNotFoundError  # noqa: PLC0415

        try:
            ZoneInfo(tz)
            return tz
        except (ZoneInfoNotFoundError, IsADirectoryError) as e:
            raise InvalidDataError("Invalid IANA timezone string") from e
    else:
        try:
            from tzlocal import get_localzone_name  # noqa: PLC0415

            return get_localzone_name()
        except ModuleNotFoundError:
            print(
                "Warning: No timezone specified and tzlocal not found. "
                "Setting timezone as the fallback value: 'Etc/UTC'"
            )
            return "Etc/UTC"


def normalise_timestamps(
    series: pd.Series, *, tz: str | None = None, unit: str | None = None
) -> pd.Series:
    """
    Convert series values to tz-aware pd.Timestamp.
    """
    try:
        if not pd.api.types.is_numeric_dtype(series):
            unit = None
        series = pd.to_datetime(series, unit=unit, utc=True)
    except ValueError as e:
        raise InvalidDataError(e)
    else:
        tz = validate_tz(tz)
    if hasattr(series, "dt.tz") and series.dt.tz is None:
        series = series.dt.tz_localize(tz)
    else:
        series = series.dt.tz_convert(tz)
    return series


def check_datetime(
    date: str | pd.Timestamp | datetime.datetime,
    tz: str | None = None,
    unit: str | None = None,
) -> pd.Timestamp:
    """
    Convert date to timezone aware pandas Timestamp
    """
    if tz is None:
        try:
            from tzlocal import get_localzone_name  # noqa: PLC0415

            tz = get_localzone_name()
        except ModuleNotFoundError:
            print(
                "Warning: No timezone specified and tzlocal not found. "
                "Setting timezone as the default value: 'Etc/UTC'"
            )
            tz = "Etc/UTC"
    if not hasattr(date, "tzinfo") or date.tzinfo is None:
        date = pd.Timestamp(date, tz=tz, unit=unit)
    else:
        date = pd.Timestamp(date)
    return date
