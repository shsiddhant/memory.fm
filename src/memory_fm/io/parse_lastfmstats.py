"""Module: memory_fm.ingest.parse_lastfmstats_com

Read pandas DataFrame from obtained from parsing lastfmstats-username.json,
check neccesary column properties ('username', 'scrobbles'), and extract the nested data from scrobbles column as a DataFrame.

Example of a valid lastfmstats-username.json (optional column "albumId")
------------------------------------------------------------------------------
{"username":"lazulinoother", "scrobbles":[{"track":"They'll Only Miss
You When You Leave","artist":"Carissa's Wierd","album":"Songs About Leaving",
"albumId":"948a8a4c-23f3-4bf2-b201-dcb68a89b897","date":1757352413000}]}
------------------------------------------------------------------------------

Corresponding DataFrame base_df obtained using utils.loaders.parse_json

Functions: verify_columns,
           extract_scrobble_dataframe,
           verify_scrobbles_columns
"""

import pandas as pd
from memory_fm.exceptions import SchemaError


def verify_columns(base_df):
    """

    """
    for column in ['username', 'scrobbles']:
        if column not in base_df.columns:
            raise SchemaError(f"Column not found: '{column}'", column)
    try:
        if base_df['username'].nunique() != 1:
            raise SchemaError("Column 'username' must contain exactly one unique value", 'username')
    except TypeError as e:
        raise SchemaError("Hashable values expected in column 'username'", 'username') from e


def extract_scrobble_dataframe(base_df):
    """

    """
    verify_columns(base_df)
    username = base_df.loc[0, 'username']
    try:
        scrobble_df = base_df['scrobbles'].apply(pd.Series)
        # Convert 'date' from int to datetime
        if 'date' in scrobble_df.columns:
            scrobble_df['date'] = pd.to_datetime(scrobble_df['date'],
                                                        unit='ms')
    except TypeError as e:
        raise SchemaError(f"Column 'scrobbles': {e}", 'scrobbles') from e
    scrobble_data = {'username': f"{username}", 'scrobbles': scrobble_df} 
    return scrobble_data


def verify_scrobbles_columns(scrobble_data,
                            scrobbles_required_columns=['track', 'artist', 'album', 'date']):
    """

    """
    scrobble_df = scrobble_data['scrobbles']
    for column in scrobbles_required_columns:
        if column not in scrobble_df.columns:
            raise SchemaError(f"Column not found inside the 'scrobbles' key: '{column}'", column)
