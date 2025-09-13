"""Module: memory_fm.normalise.normalise_lastfmstats
"""

#import pandas as pd
from memory_fm.exceptions import SchemaError
from ..ingest import parse_lastfmstats

def verify_scrobble_data_keys(scrobble_data):
    """
    """
     
    try:
        keys = scrobble_data.keys()
    except AttributeError as e:
        raise SchemaError("Expected dict-like argument") from e
    if 'username' not in keys:
        raise SchemaError("Key not found", 'username')
    if 'scrobbles' not in keys:
        raise SchemaError("Key not found", 'scrobbles')

def normalise(scrobble_data):
    """
    """
    verify_scrobble_data_keys(scrobble_data)
    parse_lastfmstats.verify_scrobbles_columns(scrobble_data)
    scrobble_df = scrobble_data['scrobbles']
    if 'albumId' in scrobble_df.columns:
        scrobble_df.pop('albumId')
    scrobble_df = scrobble_df.rename(str.capitalize, axis='columns')
    scrobble_df = scrobble_df.loc[:, ['Date', 'Track', 'Artist', 'Album']]
    scrobble_data['scrobbles'] = scrobble_df
    return scrobble_data
