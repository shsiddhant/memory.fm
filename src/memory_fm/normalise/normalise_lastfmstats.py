"""Module: memory_fm.normalise.normalise_lastfmstats
"""

#import pandas as pd
#from memory_fm import exceptions

def normalise(scrobble_df):
    """
    """
    if 'albumId' in scrobble_df.columns:
        scrobble_df.pop('albumId')
    else:
        print("")
    scrobble_df_new = scrobble_df.rename(str.capitalize, axis='columns')
    return scrobble_df_new
