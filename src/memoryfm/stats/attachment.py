from __future__ import annotations
from typing import TYPE_CHECKING
from math import log, exp
import numpy as np
import pandas as pd

if TYPE_CHECKING:
    from numpy.typing import NDArray
    from memoryfm import ScrobbleLog
    from typing import Literal


def renyi_entropy(
    counts: list[int] | tuple[int, ...] | NDArray[np.int64] | pd.Series,
    alpha: np.float64 = 1,
) -> np.float64 | None:
    """
    Compute Rényi entropy from an iterable of counts/proportions.

    Parameters
    ----------
    counts : list[int], tuple[int], NDArray[np.int64]
        A list, tuple, or numpy array containing positive integer counts.
    alpha : np.float64
        A positive floating point value, representing the order of Rényi entropy.

    Returns
    -------
    np.float64, np.nan
        Returns the Rényi entropy. If empty list/array, returns np.nan.

    """
    if not len(counts):
        return np.nan
    try:
        alpha = np.float64(alpha)
    except ValueError:
        raise ValueError("alpha must be a floating point")
    if alpha < 0:
        raise ValueError("alpha must be non-negative")
    try:
        counts = np.array(counts, dtype=np.int64, ndmin=1)
    except ValueError:
        raise ValueError("All values must be non-negative integers")
    if counts[counts < 0].size:
        raise ValueError("All values must be non-negative integers")
    elif not counts[counts > 0].size:
        raise ValueError("There must be atleast one non-zero value.")
    prop = counts / np.sum(counts)
    if alpha != 1:
        renyi = (1 / (1 - alpha)) * log(np.sum(prop**alpha))
    elif alpha == 1:
        renyi = -np.sum(prop * np.log(prop))
    return renyi


def attachment_index_counts(
    counts: list[int] | tuple[int, ...] | NDArray[np.int64] | pd.Series,
    alpha: np.float64 = 1,
) -> np.float64 | np.nan | None:
    """
    Compute Attachment Index from an iterable of counts/proportions.

    Attachment Index is always between 0 and 100.

    Parameters
    ----------
    counts : list[int], tuple[int], NDArray[int64]
        A list, tuple, or numpy array containing positive integer counts.
    alpha : float64
        A positive floating point value, representing the order of Rényi entropy.

    Returns
    -------
    np.float64, np.nan
        Returns the Attachment Index. If empty list/array, returns np.nan.

    """
    renyi = renyi_entropy(counts, alpha)
    return 100 * exp(-renyi)


def attachment_index_list(
    sample: list | tuple | NDArray | pd.Series,
    alpha: np.float64 = 1,
) -> np.float64 | np.nan | None:
    """
    Compute Attachment Index from an iterable of values.

    Attachment Index is always between 0 and 100.

    Parameters
    ----------
    sample : list, tuple, NDArray, pd.Series
        A list, tuple, numpy array, or pandas series containing all values (
        for example artists, albums, or tracks)
    alpha : float64
        A positive floating point value, representing the order of Attachment Index.

    Returns
    -------
    np.float64, np.nan
        Returns the Attachment Index. If empty list/array, returns np.nan.

    """
    counts = np.unique(sample, return_counts=True)[1]
    return attachment_index_counts(counts, alpha)


def attachment(
    sclog: ScrobbleLog,
    by: Literal["track", "artist", "album"] = "track",
    freq: str | pd.Period = "D",
    year: int | None = None,
    alpha: np.float64 = 1,
) -> pd.Series:
    """
    Compute Attachment Index from a ScrobbeLog

    Attachment Index is always between 0 and 100.

    Parameters
    ----------
    sclog : ScrobbleLog
        a memoryfm ScrobbleLog
    by : track, artist, album, default track
        The field to use for calculating Attachment Index.
    freq : str, pd.Period, default D
        The time frequency to use for the weighted attachment index. For instance,
        "3D" means a attachment index is calculated once for every 3 days.
        one value for every two weeks.
        For a full description,
        see `pandas period aliases <https://pandas.pydata.org/docs/user_guide/timeseries.html#period-aliases>`_
    year : int, Optional
        The year to use for filtering. If ``None`` or not passed, no filtering is done.
    alpha : np.float64, default 1
        A positive floating point value, representing the order of Attachment Index.

    Returns
    -------
    pd.Series
        Returns a pandas series containing Attachment Index for each period.

    """
    series = sclog.df[by].copy()
    # series.index = sclog.df["timestamp"].dt.to_period(freq=freq)
    series.index = sclog.df["timestamp"]
    series = series.dropna()
    att_index_func = np.vectorize(attachment_index_list, otypes=[np.float64])
    groupedlist = series.resample(rule=freq, closed="left", label="left").agg(list)
    attachment_index = pd.Series(att_index_func(groupedlist, alpha))
    attachment_index.index = groupedlist.index
    if year is not None:
        attachment_index = attachment_index[attachment_index.index.year == year]
    return attachment_index


def weighted_attachment(
    sclog: ScrobbleLog,
    by: Literal["track", "artist", "album"] = "track",
    freq: str | pd.Period = "W",
    year: int | None = None,
    alpha: np.float64 = 1,
) -> pd.Series:
    """
    Calculate weighted attachment index.

    The Weights are given by ``log2(1+r)``,
    where r is the ratio of scrobbles in a period and
    maximum number of scrobbles in all periods for the frequency.

    Parameters
    ----------
    sclog : ScrobbleLog
        a memoryfm ScrobbleLog
    by : track, artist, album
        The field to use for calculating the weighted Attachment Index.
    freq : str, pd.Period
        The time frequency to use for the weighted attachment index. For instance,
        "2W" means a attachment index is calculated bi-weekly i.e.
        one value for every two weeks.
        For a full description,
        see `pandas period aliases <https://pandas.pydata.org/docs/user_guide/timeseries.html#period-aliases>`_
    year : int, Optional
        The year to use for filtering. If ``None`` or not passed, no filtering is done.
    alpha : np.float64
        A positive floating point value, representing the order of Attachment Index.

    Returns
    -------
    pd.Series
        Returns a pandas Series containing weighted Attachment Index for each period.

    """
    series = sclog.df[by].copy()
    series.index = sclog.df["timestamp"]
    series = series.dropna()
    scrobblecounts = series.resample(rule=freq, closed="left", label="left").agg(len)
    weighted_attachment_index = np.log2(
        1 + scrobblecounts / scrobblecounts.max()
    ) * attachment(sclog, by, freq, year, alpha)
    if year is not None:
        weighted_attachment_index = weighted_attachment_index[
            weighted_attachment_index.index.year == year
        ]
    weighted_attachment_index = weighted_attachment_index.fillna(0)
    return weighted_attachment_index


def hill_number_counts(
    counts: list[int] | tuple[int, ...] | NDArray[np.int64] | pd.Series,
    alpha: np.float64 = 1,
) -> np.float64 | np.nan | None:
    """
    Calculate Hill number from an iterable of counts/proportions.

    Parameters
    ----------
    counts : list[int], tuple[int], NDArray[np.int64]
        A list, tuple, or numpy array containing positive integer counts.
    alpha : np.float64
        A positive floating point value, representing the order of Rényi entropy.

    Returns
    -------
    np.float64, np.nan
        Returns the Hill number. If empty list/array, returns np.nan.

    """
    att_index = attachment_index_counts(counts, alpha)
    if att_index:
        return 100 / att_index
    else:
        return np.nan


def hillnumber(
    sclog: ScrobbleLog,
    by: Literal["track", "artist", "album"] = "track",
    freq: str | pd.Period = "W",
    year: int | None = None,
    alpha: np.float64 = 1,
) -> np.NDArray[np.float64 | np.nan] | None:
    """
    Compute Hill numbers from a ScrobbeLog

    Hill numbers roughly represent average number of distinct values/species like
    artists, albums, and tracks in our case.

    Parameters
    ----------
    sclog : ScrobbleLog
        a memoryfm ScrobbleLog
    by : track, artist, album
        The field to use for calculating Hill numbers.
    freq: str, pd.Period
        The time frequency to use for Hill numbers. For instance,
        "2W" means Hill numbers are calculated bi-weekly i.e. one value for every
        two weeks. For a full description,
        see `pandas period aliases <https://pandas.pydata.org/docs/user_guide/timeseries.html#period-aliases>`_
    year : int, Optional
        The year to use for filtering. If ``None`` or not passed, no filtering is done.
    alpha : np.float64
        A positive floating point value, representing the order of the Hill numbers.

    Returns
    -------
    pd.Series
        Return a pandas Series containing the Hill numbers for each period.

    """
    return 100 / attachment(sclog, by, freq, year, alpha)
