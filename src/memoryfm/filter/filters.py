"""
"""

import datetime
from typing import TYPE_CHECKING
from memoryfm.errors import SchemaError

if TYPE_CHECKING:
    import pandas as pd


def _date_filter(
    scrobble_df: pd.DataFrame,
    start: datetime.datetime,
    end: datetime.datetime,
    include_end=True
) ->pd.DataFrame:
    """
    Filter Scrobble DataFrame by date.
    """
    if include_end:
        end = end + datetime.timedelta(days=1)

    if 'timestamp' not in scrobble_df.columns:
        raise SchemaError("Expected column 'timestamp' missing",
                                 'timestamp')
    filter_start = scrobble_df['timestamp'] >= start
    filter_end = scrobble_df['timestamp'] < end
    filter_condition = filter_start & filter_end
    date_filtered_df = scrobble_df[filter_condition]
    
    return date_filtered_df
