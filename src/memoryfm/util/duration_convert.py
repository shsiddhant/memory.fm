import pandas as pd


def ms_to_time(ms_series: pd.Series) -> pd.Series:
    seconds = ms_series // 1000
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)

    duration = [series.astype(str).str.zfill(2) for series in [hours, minutes, seconds]]
    dur = duration[0].str.cat([duration[1], duration[2]], sep=":")
    return dur
