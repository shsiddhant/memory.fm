"""Module: memory_fm.ingest.parse_lastfmstats_json

Read pandas DataFrame from obtained from parsing lastfmstats-username.json,
check neccesary column properties ('username', 'scobbles'), extract and
return the nested DataFrame from the scrobbles column.

Example of a valid lastfmstats-username.json (optional column "albumId")
------------------------------------------------------------------------------
{"username":"lazulinoother", "scrobbles":[{"track":"They'll Only Miss
You When You Leave","artist":"Carissa's Wierd","album":"Songs About Leaving",
"albumId":"948a8a4c-23f3-4bf2-b201-dcb68a89b897","date":1757352413000}]}
------------------------------------------------------------------------------

Functions: verify_columns, extract_scrobble_dataframe
"""

import pandas as pd
from ..ingest.check_json_validity import InvalidDataError


def verify_columns(log_df):
    """

    """
    columns = log_df.columns
    if 'username' not in columns:
        raise InvalidDataError("Column 'username' not found")
    elif 'scrobbles' not in columns:
        raise InvalidDataError("Column 'scrobbles' not found")
    elif log_df['username'].nunique() != 1:
        raise InvalidDataError("Column 'username' must contain exactly one unique value")
    
    return log_df


def extract_scrobble_dataframe(log_df):
    """

    """
    try:
        verified_log_df = verify_columns(log_df)
        scrobble_log_df = verified_log_df['scrobbles'].apply(pd.Series)

    except TypeError as e:
        if "'set' type is unordered" in str(e):
            raise InvalidDataError("Column 'scrobbles' contains an unordered element of 'set' type")
        else:
            raise

    return scrobble_log_df
