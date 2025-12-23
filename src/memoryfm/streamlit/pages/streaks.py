from __future__ import annotations
from typing import TYPE_CHECKING
import streamlit as st

if TYPE_CHECKING:
    from memoryfm import ScrobbleLog
    import plotly.graph_objects as go

from memoryfm.streamlit.util import set_session_data
from memoryfm.streamlit.util import format_chart_type
from memoryfm.stats.streaks import streaks
from memoryfm.viz.timeline import (
    streaktimeline_interactive,
)

# Update Session State
set_session_data(st.session_state["username"])
sc_log: ScrobbleLog
sc_log = st.session_state["sc_log"]

# Reduce Padding
st.markdown(
    """
    <style>
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        padding-left: 5rem;
        padding-right: 5rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

page_name = "streaks_timeline"


# Page Layout
# --------------------------------------------------------------
# Header
st.title(":primary[:material/bolt: Streaks]")
st.write("---")
""

with st.container():
    kind_col, year_col = st.columns([1, 1], border=True)

# Select Type
with kind_col:
    st.markdown("#### :material/view_list: Type")
    kind = st.radio(
        "Pick a chart type",
        ["artists", "albums", "tracks"],
        key=page_name,
        horizontal=True,
        label_visibility="collapsed",
        format_func=format_chart_type,
    )
    kind_2 = kind.rstrip("s")

all_years = sc_log.df.timestamp.dt.year.unique()

# Select Year
with year_col:
    st.markdown("#### :material/calendar_month: Year")
    year = st.select_slider(
        "Year",
        all_years,
        value=all_years[-1],
        label_visibility="collapsed",
    )

"---"

# Longest Streak(s)
with st.container():
    st.write(f"### Longest {kind_2.capitalize()} Streak")
    streaks_df = streaks(sc_log, kind_2)
    start_filter = streaks_df.start.dt.year == year
    end_filter = streaks_df.end.dt.year == year
    date_filter = start_filter | end_filter
    streaks_df = streaks_df[date_filter]
    streaks_df = streaks_df.rename(columns=lambda x: x.capitalize())
    streaks_df = streaks_df.dropna()
    longest_streaks = streaks_df[streaks_df.Length == streaks_df.Length.max()]
    dt_fmt = "%d %b, %Y %I:%M %p"
    for pos in ["Start", "End"]:
        longest_streaks[pos] = longest_streaks[pos].dt.strftime(dt_fmt)
    st.markdown(longest_streaks.to_markdown(index=False))

"---"

# Streaks Timeline
with st.container():
    st.write(f"### {kind_2.capitalize()} Streaks Timeline")
    fig: go.Figure
    fig = streaktimeline_interactive(sc_log, kind_2, year=year, minlength=10)
    fig.update_layout(paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF")
    st.plotly_chart(fig, theme=None)
