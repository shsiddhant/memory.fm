"""
"""

from datetime import timedelta
#import pandas as pd
from memory_fm import exceptions

def date_filter(scrobble_df, begin_date, end_date, include_end_date=True):
    """

    """
    if include_end_date:
        end_date = end_date + timedelta(days=1)

    if 'Date' not in scrobble_df.columns:
        raise exceptions.SchemaError("Expected column 'Date' missing", 'Date')
    filter_start = scrobble_df['Date'] >= begin_date
    filter_end = scrobble_df['Date'] < end_date
    filter_condition = filter_start & filter_end
    date_filtered_df = scrobble_df[filter_condition]
    
    return date_filtered_df
