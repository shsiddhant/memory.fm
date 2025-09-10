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
from memory_fm.exceptions import SchemaError


def verify_columns(log_df):
    """

    """
    for column in ['username', 'scrobbles']:
        if column not in log_df.columns:
            raise SchemaError(f"Column not found: '{column}'", column)
    if log_df['username'].nunique() != 1:
        raise SchemaError("Column 'username' must contain exactly one unique value", 'username')
    
    return log_df


def extract_scrobble_dataframe(log_df):
    """

    """
    try:
        verified_log_df = verify_columns(log_df)
        scrobble_log_df = verified_log_df['scrobbles'].apply(pd.Series) 
        # Convert 'date' from int to datetime
        if 'date' in scrobble_log_df.columns:
            scrobble_log_df['date'] = pd.to_datetime(scrobble_log_df['date'], unit='ms')
    except TypeError as e:
        if "'set' type is unordered" in str(e):
            raise SchemaError("Column 'scrobbles' contains an unordered element of 'set' type", 'scrobbles')
        else:
            raise
    return scrobble_log_df

def verify_scrobbles_columns(scrobble_log_df,
                            scrobbles_columns=['track', 'artist', 'album', 'date']):
    """

    """
    columns = scrobble_log_df.columns
    for column in scrobbles_columns:
        if column not in columns:
            raise SchemaError(f"Column not found inside the 'scrobbles' key: '{column}'", column)

    return scrobble_log_df
