from __future__ import annotations
from typing import TYPE_CHECKING
import numpy as np
import pandas as pd
from memoryfm._cython._streaks import streak_gen

if TYPE_CHECKING:
    import memoryfm as mfm
    from typing import Literal
    from datetime import datetime

    ArrayLike = list | tuple | np.typing.NDArray | pd.Series


def gen_streak_bool(series: ArrayLike) -> np.NDArray:
    """
    Create boolean series after comparing consecutive values.

    Parameters
    ----------
    series : ArrayLike

    Returns
    -------
    np.NDArray
        Returns the boolean array of consecutive value comparisions.

    """
    series = np.array(series.factorize()[0])
    bool_ser = np.array((series[1:] == series[:-1]), dtype=np.intc)
    return bool_ser


def streaks(
    sclog: mfm.ScrobbleLog,
    kind: Literal["album", "artist", "track"],
    minlength: int = 10,
    start: str | pd.Timestamp | datetime | None = None,
    end: str | pd.Timestamp | datetime | None = None,
) -> pd.DataFrame:
    """
    Find streaks of artists/albums/tracks from a ScrobbleLog.

    Parameters
    ----------
    sclog : ScrobbleLog
        The ScrobbleLog from which to search for streaks.
    kind : album, artist, or track
        The kind of streaks to find - artist, album or track.
    minlength : int, default 10
        The minimum length that the streaks must have. Any streaks below this length
        are discarded.
    start : str, pd.Timestamp, default None
        An optional start date to filter the ScrobbleLog. Either a string representing
        a datetime,  a datetime object or a pandas Timestamp object.
    end : str, pd.Timestamp, default None
        An optional end date to filter the ScrobbleLog. Either a string representing
        a datetime,  a datetime object or a pandas Timestamp object.

    """
    kinds = {"track": 1, "artist": 2, "album": 3}
    col = kinds[kind]
    if start is None and end is None:
        df = sclog.df
    else:
        df = sclog.filter_by_date(start, end).df
    streak_start = gen_streak_bool(df.loc[:, kind])
    streaks_arr = np.array(streak_gen(streak_start, minlength))
    streaks = pd.DataFrame(streaks_arr, columns=["start", "end", "length"])
    streaks[kind] = streaks.start.map(lambda x: df.iloc[x, col])
    streaks["start"] = streaks.start.map(lambda x: df.iloc[x, 0])
    streaks["end"] = streaks.end.map(lambda x: df.iloc[x, 0])
    return streaks
