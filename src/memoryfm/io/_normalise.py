"""Module: memoryfm.normalise.normalise_lastfmstats
"""
from __future__ import annotations
import pandas as pd
from memoryfm.errors import SchemaError, InvalidDataError
from memoryfm.core.objects import ScrobbleLog

def normalise_timestamps(
    series: pd.Series,
    *,
    tz: str | None = None,
    unit: str | None = None
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
        from memoryfm.core._validation import validate_tz
        tz = validate_tz(tz)
    if hasattr(series, "dt.tz") and series.dt.tz is None:
        series = series.dt.tz_localize(tz)
    else:
        series = series.dt.tz_convert(tz)
    return series

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
                                          unit="ms")
    else:
        raise SchemaError("Column not found", 'date')
    df = df.rename(columns={'date':'timestamp'})
    log = ScrobbleLog(df=df, username=username,
                      tz=tz, source="lastfmstats.com")
    return log
