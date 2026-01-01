from __future__ import annotations
from typing import TYPE_CHECKING
from memoryfm.stats.attachment import (
    weighted_attachment,
    # hillnumber,
)
import plotly.graph_objects as go

if TYPE_CHECKING:
    from memoryfm import ScrobbleLog
    import pandas as pd
    import numpy as np
    from typing import Literal


def weighted_attachment_plot(
    sclog: ScrobbleLog,
    by: Literal["track", "artist", "album"] = "track",
    freq: str | pd.Period = "D",
    year: int | None = None,
    alpha: np.float64 = 1,
    window: str = "7D",
    color: str = "orange",
    rollingcolor: str = "red",
) -> go.Figure:
    """
    Plot Attachment and Weighted Attachment Indices.

    Parameters
    ----------
    sclog : ScrobbleLog
        a memoryfm ScrobbleLog
    by : track, artist, album, default track
        The field to use for calculating the weighted Attachment Index.
    freq : str, pd.Period, default D
        The time frequency to use for the weighted attachment index. For instance,
        "3D" means a attachment index is calculated once for every 3 days.
        For a full description,
        see `pandas period aliases <https://pandas.pydata.org/docs/user_guide/timeseries.html#period-aliases>`_
    year : int, Optional
        The year to use for filtering. If ``None`` or not passed, no filtering is done.
    alpha : np.float64, default 1
        A positive floating point value, representing the order of Attachment Index.
    window : str, pd.Period, default 7D
        The window for rolling averages. For full description,
        see `pandas period aliases <https://pandas.pydata.org/docs/user_guide/timeseries.html#period-aliases>`_
    color : str, default orange
        The color of the weighted attachment line plot.
    rollingcolor : str, default red
        The color of the rolling averages plot.

    Returns
    -------
    go.Figure
        A plotly Figure containing the weighted attachment index and rolling
        averages plots.
    """
    watt_in = weighted_attachment(sclog, by, freq, year, alpha)
    rolling_watt_in = watt_in.rolling(window).mean()
    fig = go.Figure()
    watt_in_plot = go.Scatter(
        x=watt_in.index,
        y=watt_in,
        mode="lines",
        name="Weighted Attachment Index",
        line={"color": color, "dash": "dot"},
    )
    rolling_plot = go.Scatter(
        x=watt_in.index,
        y=rolling_watt_in,
        mode="lines",
        name="7-Day Rolling Averages",
        line={"color": rollingcolor},
    )
    fig.add_traces([watt_in_plot, rolling_plot])
    return fig


# def hillnumber_plot():
