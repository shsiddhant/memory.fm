from __future__ import annotations
from typing import TYPE_CHECKING
import numpy as np
from pandas import Timestamp
from pathlib import Path
from memoryfm.stats.streaks import streaks
import matplotlib.pyplot as plt
from matplotlib.colors import FuncNorm
import matplotlib.dates as mdates
from matplotlib import cm
import plotly.express as px

if TYPE_CHECKING:
    from memoryfm import ScrobbleLog
    from typing import Literal
    import matplotlib.figure as mfigure
    import plotly.graph_objects as go


def streaktimeline_static(
    sclog: ScrobbleLog,
    kind: Literal["artist", "album", "track"],
    minlength: int = 10,
    year: int = 2025,
    showcbar: bool = True,
    savedir: str | Path | None = None,
) -> mfigure.Figure:
    """
    Create a static Streaks Timeline for a ScrobbleLog.

    Parameters
    ----------
    sclog : ScrobbleLog
        A ScrobbleLog for which the streaks timeline needs to be created.
    kind : album, artist, or track
        The kind of streaks timeline to create - artist, album or track.
    minlength : int, default 10
        The minimum length that the streaks must have. Any streaks below this length
        are discarded.
    year : int, default 2025
        The year for which the streaks timeline needs to be created.
    showcbar : bool, default True
        Show a colorbar showing the color and streak length scale.
    savedir : str, Path, default None
        The path to the directory to save the timeline image.

    Returns
    -------
    matplotlib.figure.Figure
        A matplotlib figure containing the streaks timeline plot.

    """
    _forward = np.vectorize(lambda x: np.log2(x) if x > 0 else 0, otypes=[float])
    _inverse = np.vectorize(lambda x: 2**x, otypes=[float])
    streaksdf = streaks(
        sclog, kind=kind, minlength=minlength, start=f"{year}", end=f"{year}-12-31"
    )
    streaksdf["duration"] = streaksdf.end - streaksdf.start
    vmax = streaksdf.length.max()
    norm = FuncNorm(functions=(_forward, _inverse), vmin=1, vmax=vmax)
    cmap = plt.colormaps["Reds"]
    fig, ax = plt.subplots(figsize=(35, 3))
    plt.rcParams["font.sans-serif"] = ["Space Grotesk"]
    xrange = np.array(streaksdf.loc[:, ["start", "duration"]])
    ax.broken_barh(xrange, (0, 1), color=cmap(norm(streaksdf.length)))
    ax.set_title(
        label=f"Streaks Timeline - {kind.capitalize()}s\n{year}\n",
        fontsize="x-large",
    )
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
    ax.set_yticks([])
    ax.set_xlim(
        Timestamp(f"{year}", tz=sclog.tz), Timestamp(f"{year}-12-31", tz=sclog.tz)
    )
    if showcbar:
        cbar = fig.colorbar(
            cm.ScalarMappable(norm=norm, cmap=cmap),
            label="Streak Length",
            ax=ax,
            location="bottom",
            pad=0.5,
            aspect=100,
        )
        cbar.ax.annotate(
            f"{vmax}",
            xy=(1, 0.8),
            xytext=(1.005, 0.4),
            xycoords="axes fraction",
            textcoords="axes fraction",
        )
        ticks = [2**k for k in np.arange(np.ceil(np.log2(vmax)), dtype=int)]
        ticks.sort()
        cbar.set_ticks(ticks)
    plt.xticks(rotation=45)
    plt.tight_layout()
    if savedir is not None:
        plt.savefig(
            Path(savedir).resolve() / f"{sclog.username}-{year}-{kind}.png", dpi=150
        )
    return fig


def streaktimeline_interactive(
    sclog: ScrobbleLog,
    kind: Literal["artist", "album", "track"],
    minlength: int = 10,
    year: int = 2025,
) -> go.Figure:
    """
    Create an interactive Streaks Timeline for a ScrobbleLog.

    Parameters
    ----------
    sclog : ScrobbleLog
        A ScrobbleLog for which the streaks timeline needs to be created.
    kind : album, artist, or track
        The kind of streaks timeline to create - artist, album or track.
    minlength : int, default 10
        The minimum length that the streaks must have. Any streaks below this length
        are discarded.
    year : int, default 2025
        The year for which the streaks timeline needs to be created.
    showcbar : bool, default True
        Show a colorbar showing the color and streak length scale.
    savedir : str, Path, default None
        The path to the directory to save the timeline image.

    Returns
    -------
    go.Figure
        A Plotly figure containing the streaks timeline plot.

    """
    streaksdf = streaks(
        sclog, kind=kind, minlength=minlength, start=f"{year}", end=f"{year}-12-31"
    )
    size = len(streaksdf)
    vmax = streaksdf.length.max()
    fig = px.timeline(
        streaksdf,
        x_start="start",
        x_end="end",
        color=np.log2(streaksdf.length),
        hover_name=kind,
        hover_data=["start", "end", "length"],
        y=size * [1],
        color_continuous_scale=px.colors.sequential.Reds,
        range_color=[0, np.log2(vmax)],
        custom_data=["length", kind],
    )
    fig.update_yaxes(visible=False, showticklabels=False)
    tickvals = np.arange(np.ceil(np.log2(vmax)), dtype=int)
    ticktext = [f"{2**k}" for k in tickvals]
    fig.update_coloraxes(
        colorbar={
            "tickvals": tickvals,
            "ticktext": ticktext,
            "title": "Streak Length",
            "orientation": "h",
        },
    )
    fig.update_traces(
        hovertemplate=(
            f"<b>{kind.capitalize()}:</b> %{{customdata[1]}}<br>"
            "<b>Start:</b> %{base}<br>"
            "<b>Finish:</b> %{x}<br>"
            "<b>Length:</b> %{customdata[0]}"
            "<extra></extra>"
        )
    )
    return fig
