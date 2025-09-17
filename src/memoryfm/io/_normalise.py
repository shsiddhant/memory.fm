"""Module: memoryfm.normalise.normalise_lastfmstats
"""

import pandas as pd
from memoryfm.errors import SchemaError
from memoryfm.core.objects import ScrobbleLog


def normalise_lastfmstats(username: str,
                          scrobble_df: pd.DataFrame) -> ScrobbleLog:
    """
    """
    scrobble_df = scrobble_df.rename(str.lower, axis=1)
    # Convert 'date' from int to datetime
    if 'date' in scrobble_df.columns:
        scrobble_df['date'] = pd.to_datetime(scrobble_df['date'],
                                                  unit='ms')
    else:
        raise SchemaError("Column not found", 'date')
    scrobble_df =scrobble_df.rename(columns={'date':'timestamp'})
   # for column in scrobble_df.columns:
   #     if column not in ["timestamp",
   #                       "track",
   #                       "artist",
   #                       "album"]:
   #         scrobble_df.pop(column)
    scrobble_df = scrobble_df[["timestamp", "track", "artist", "album"]]
    return ScrobbleLog(username, scrobble_df)
