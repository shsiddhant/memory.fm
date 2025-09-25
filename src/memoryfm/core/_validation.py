from __future__ import annotations
import pandas as pd
from memoryfm.errors import (
    SchemaError,
    InvalidDataError,
    InvalidTypeError
)

def validate_df(
    df: pd.DataFrame,
    tz: str | None
) -> pd.DataFrame:
    """
    Validate ScrobbleLog DataFrame
    """
    if not isinstance(df, pd.DataFrame):
        raise InvalidTypeError("Expecting a pandas DataFrame.")
    required_columns = [
        "timestamp",
        "track",
        "artist"
    ]
    for column in required_columns:
        if column not in df.columns:
            raise SchemaError(
                f"Required DataFrame column not found: {column}",
                column
            )
    df = df.dropna(subset=required_columns)
    if not df.empty:
        tz = validate_tz(tz)
        from memoryfm.io._normalise import normalise_timestamps
        with pd.option_context('mode.copy_on_write', True):
            df["timestamp"] = normalise_timestamps(df["timestamp"],
                                                   tz=tz, unit="ms")
    if "album" not in df.columns:
        df["album"] = None
    df = df[["timestamp", "track", "artist", "album"]]
    df = df.replace(r'^\s*$', None, regex=True)
    return df

def validate_tz(tz: str | None = None) -> str:
    """ Set timezone value from valid IANA string.

    If no value or `None` passed, tries to use tzlocal to
    get the timezone value.
    Fallback: Etc/UTC
    """
    if not isinstance(tz, str | None):
        raise InvalidTypeError("Expecting string type value for tz")
    elif tz is not None:
        from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
        try:
            ZoneInfo(tz)
            return tz
        except (ZoneInfoNotFoundError, IsADirectoryError) as e:
            raise InvalidDataError("Invalid IANA timezone string") from e
    else:
        try:
            from tzlocal import get_localzone_name
            return get_localzone_name()
        except ModuleNotFoundError:
            print(
                "Warning: No timezone specified and tzlocal not found. "
                "Setting timezone as the fallback value: 'Etc/UTC'"
            )
            return "Etc/UTC"

def validate_text(
    text: str,
    field: str
) -> str:
    """
    """ 
    
    if not isinstance(text, str | None):
        raise InvalidTypeError(f"Expecting string value for {text}")
    elif text is not None and not text.strip():
        raise InvalidDataError(f"{field} cannot be just white-space")
    else:
        return text


def meta_generator(
    df: pd.DataFrame,
    username: str | None = None,
    tz: str | None = "Etc/UTC",
    source: str | None = "manual"
) -> dict:
    """
    Generate metadata for ScrobbleLog init
    """
    if not isinstance(df, pd.DataFrame):
        raise InvalidTypeError("Expecting a pandas DataFrame")
    from importlib.metadata import version
    meta = {
        "username": validate_text(username, "username"),
        "tz": validate_tz(tz),
        "num_scrobbles": len(df),
        "date_range": {
            "start": None,
            "end": None
        },
        "source": source,
        "memory.fm_version": f"{version('memory.fm')}",
        "schema_version": 1
    }
    if source is None:
        meta["source"] = "manual"
    if len(df):
        if "timestamp" in df.columns:
            meta["date_range"]["start"] = df["timestamp"].min().isoformat()
            meta["date_range"]["end"] = df["timestamp"].max().isoformat()
        else:
            raise SchemaError("Missing required column: timestamp",
                              "timestamp")
    meta = validate_meta(meta)
    return meta

def validate_meta(meta: dict) -> dict:
    """
    Validate meta schema
    """
    types = {
        "username": [str, "str"],
        "tz": [str, "str"],
        "memory.fm_version": [str, "str"],
        "schema_version": [int, "int"],
        "num_scrobbles": [int, "int"],
        "date_range": [dict, "dict"],
        "source": [str, "str"]
    }
    if not isinstance(meta, dict):
        raise InvalidTypeError("Expecting a dict type value")
    for key in types.keys():
        if key not in meta.keys():
            raise SchemaError(f"Missing key: {key}", key)
        elif not isinstance(meta[key], types[key][0]):
            raise InvalidTypeError(
                f"Expecting {types[key][1]} type value for key: {key}]", key)
    meta["username"] = validate_text(meta["username"], "username")
    meta["tz"] = validate_tz(meta["tz"])
    if meta["num_scrobbles"] < 0:
        raise InvalidDataError("Expecting non-negative integer value for key: "
                          "num_scrobbles", "num_scrobbles")
    for key in ["start", "end"]:
        if key not in meta["date_range"].keys():
            raise SchemaError(
                f'meta["date_range"] key not found: {key}', key)
        elif (
            meta["num_scrobbles"] > 0 and
            not isinstance(meta["date_range"][key], str)
        ):
            raise InvalidTypeError('Expecting string type value for: '
                              f'meta["date_range"]["{key}"]')
        elif (not meta["num_scrobbles"] and
              meta["date_range"][key] is not None):
            raise InvalidDataError('If num_scrobbles is 0, '
                              f'{key} must be None type')
    if {"start", "end"} != set(meta["date_range"].keys()):
        raise SchemaError("date_range keys must be one of these : "
                          "'start', 'end'")
    if not meta["source"].strip():
        raise InvalidDataError("source only contains white-space")
    return meta
