"""Module: memoryfm.normalise.normalise_lastfmstats
"""

import pandas as pd
from tzlocal import get_localzone_name
from memoryfm.errors import SchemaError
from memoryfm.core.objects import ScrobbleLog


def normalise_lastfmstats(username: str,
                          scrobble_df: pd.DataFrame) -> ScrobbleLog:
    """
    """
    scrobble_df = scrobble_df.rename(str.lower, axis=1)
    # Convert 'date' from int to datetime
    if 'date' in scrobble_df.columns:
        try:
            scrobble_df['date'] = pd.to_datetime(scrobble_df['date'],
                                                  unit='ms', utc=True)
            scrobble_df['date'] = scrobble_df['date'].dt.tz_convert(get_localzone_name())
        except ValueError as e:
            raise SchemaError(e, 'date')
    else:
        raise SchemaError("Column not found", 'date')
    scrobble_df =scrobble_df.rename(columns={'date':'timestamp'})
    return ScrobbleLog(username, scrobble_df)
