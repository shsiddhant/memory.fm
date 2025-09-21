"""Module: memoryfm.normalise.normalise_lastfmstats
"""

import pandas as pd
from memoryfm.errors import SchemaError
from memoryfm.core.objects import ScrobbleLog


def normalise_timestamps(
    series: pd.Series,
    *,
    tz: str |None = None,
    unit: str | None = None
) ->(pd.Series, str):
    """
    Convert series values to tz-aware pd.Timestamp.
    """

    try:
        from numpy import int64
        if series.dtype != int64:
            unit = None
        series = pd.to_datetime(series, unit=unit, utc=True)
        if tz is None:
            from tzlocal import get_localzone_name
            tz = get_localzone_name()
    except ValueError as e:
        raise SchemaError(e)
    except ModuleNotFoundError:
        print(
            "Warning: No timezone specified and tzlocal not found. "
            "Setting timezone as the default value: 'Etc/UTC'"
        )
        tz = "Etc/UTC"
    if hasattr(series, "dt.tz") and series.dt.tz is None:
        series = series.dt.tz_localize()
    else:
        series = series.dt.tz_convert(tz)
    return (series, tz)


def normalise_lastfmstats(
    df: pd.DataFrame,
    username: str,
    tz: str | None = None
) -> ScrobbleLog:
    """
    """
    df = df.rename(str.lower, axis=1)
    if "date" in df.columns:
        df["date"] = normalise_timestamps(df["date"],
                                                   tz=tz,
                                                   unit="ms")[0]
        tz = normalise_timestamps(df["date"],
                                                   tz=tz,
                                                   unit="ms")[1]
    else:
        raise SchemaError("Column not found", 'date')
    df =df.rename(columns={'date':'timestamp'})
    return ScrobbleLog(df=df, username=username, tz=tz, source="lastfmstats.com")

