from __future__ import annotations
import pandas as pd
import datetime

def check_datetime(
    date: str | pd.Timestamp | datetime.datetime,
    tz: str | None = None, 
    unit : str | None = None,
) ->pd.Timestamp:
    """
    Convert date to timezone aware pandas Timestamp
    """ 
    if tz is None:
        try:
            from tzlocal import get_localzone_name
            tz = get_localzone_name()
        except ModuleNotFoundError:
            print(
                "Warning: No timezone specified and tzlocal not found. "
                "Setting timezone as the default value: 'Etc/UTC'"
            )
            tz = "Etc/UTC"
    if (
        not hasattr(date, "tzinfo") or
        date.tzinfo is None
    ):
        date = pd.Timestamp(date, tz=tz, unit=unit)
    else:
        date = pd.Timestamp(date)
    return date
