import pandas as pd
from memoryfm.errors import SchemaError, InvalidDataError


def _validate_tz(tz: str) ->None:
    """
    Check if argument is a valid IANA string
    """
    if not isinstance(tz, str):
        raise InvalidDataError("Expecting string type value for tz")
    from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
    try:
        ZoneInfo(tz)
    except ZoneInfoNotFoundError as e:
        raise InvalidDataError(e)

def _meta_generator(
    df: pd.DataFrame,
    username: str,
    tz: str,
    source: str | None = "manual"
) ->dict:
    """
    Generate metadata for ScrobbleLog init
    """
    if not isinstance(df, pd.DataFrame):
        raise InvalidDataError("Expecting a pandas DataFrame as df")
    from importlib.metadata import version
    meta = {
        "username": username,
        "tz": tz,
        "memory.fm_version": f"{version('memory.fm')}",
        "schema_version": 1,
        "num_scrobbles": len(df),
        "date_range": {
            "start": None,
            "end": None
        },
        "source": source
    }
    if source is None:
        meta["source"] = "source"
    if len(df):
        if "timestamp" in df.columns:
            meta["date_range"]["start"] = df.iloc[0]["timestamp"].isoformat()
            meta["date_range"]["end"] = df.iloc[len(df) - 1]["timestamp"].isoformat()
        else:
            raise SchemaError("Column not found: 'timestamp'", "timestamp")
    _validate_meta(meta)
    return meta

def _validate_meta(meta: dict) ->None:
    """
    Validate meta schema
    """
    key_types = {
        "username": str,
        "tz": str,
        "memory.fm_version": str,
        "schema_version": int,
        "num_scrobbles": int,
        "date_range": dict,
        "source": str
    }
    if not isinstance(meta, dict):
        raise ValueError("Expecting dict type value for meta")
    for key in key_types.keys():
        if key not in meta.keys():
            raise SchemaError(f"meta key not found: {key}", key)
        elif not isinstance(meta[key], key_types[key]):
            raise SchemaError(
                f"Expecting {key_types[key]} type value for key: {key}]",
                key
            )
    if not meta["username"].strip():
        raise SchemaError("username only contains white-space", "username")
    _validate_tz(meta["tz"])
    if meta["num_scrobbles"] < 0:
        raise SchemaError("Expecting non-negative integer value for key: "
                          "num_scrobbles", "num_scrobbles")
    for key in ["start", "end"]:
        if key not in meta["date_range"].keys():
            raise SchemaError(
                f'meta["date_range"] key not found: {key}', key)
        elif (
            meta["num_scrobbles"] > 0 and
            not isinstance(meta["date_range"][key], str)
        ):
            raise SchemaError('Expecting string type value for: '
                              f'meta["date_range"]["{key}"]', key)
        elif (not meta["num_scrobbles"] and
              meta["date_range"][key] is not None):
            raise SchemaError('If num_scrobbles is 0, '
                              f'{key} must be None type', key)
    if {"start", "end"} != set(meta["date_range"].keys()):
        raise SchemaError("date_range keys must be one of these : "
                          "'start', 'end'")
    if not meta["source"].strip():
        raise SchemaError("source only contains white-space", "source")
