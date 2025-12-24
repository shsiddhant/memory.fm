from __future__ import annotations
from typing import TYPE_CHECKING
import streamlit as st

if TYPE_CHECKING:
    from memoryfm import ScrobbleLog
    import plotly.graph_objects as go

from memoryfm.streamlit.util import set_session_data, format_chart_type, PADDING
from memoryfm.stats.streaks import streaks
from memoryfm.viz.timeline import (
    streaktimeline_interactive,
)

# Update Session State
set_session_data(st.session_state["username"])
sc_log: ScrobbleLog
sc_log = st.session_state["sc_log"]

# Reduce Padding
st.markdown(PADDING, unsafe_allow_html=True)

page_name = "streaks_timeline"


# Page Layout
# --------------------------------------------------------------
# Header
st.title(
    ":primary[:material/bolt: Streaks]",
    help="A **Streak** is a series of consecutive listens of the same "
    "artist, album, or track.",
)

with st.container():
    kind_col, year_col = st.columns([1, 1], border=True, gap="large")

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


# Calculate Streaks
streaks_df = streaks(sc_log, kind_2)
start_filter = streaks_df.start.dt.year == year
end_filter = streaks_df.end.dt.year == year
date_filter = start_filter | end_filter
streaks_df = streaks_df[date_filter]
streaks_df = streaks_df.rename(columns=lambda x: x.capitalize())
streaks_df = streaks_df.dropna()

with st.popover("What is a **Streak**?", icon=":material/info:"):
    st.write(
        "A **Streak** is a series of consecutive listens of the same "
        "artist, album, or track.",
    )


# Longest Streak(s)
""
longest_streaks = streaks_df[streaks_df.Length == streaks_df.Length.max()]
dt_fmt = "%d %b, %Y %I:%M %p"
longest_streaks = longest_streaks.copy()
for pos in ["Start", "End"]:
    longest_streaks[pos] = longest_streaks[pos].dt.strftime(dt_fmt)
st.write(f"### :blue[Longest {kind_2.capitalize()} Streak]")
with st.container(border=True):
    st.write(f"##### :red-background[:red[From {longest_streaks['Start'].iloc[0]}]]")
    st.write(f"##### :orange-background[:orange[To {longest_streaks['End'].iloc[0]}]]")
    st.write(
        "##### :violet-background[:violet["
        f"You listened to {longest_streaks[kind_2.capitalize()].iloc[0]}"
        "]]"
    )
    st.write(
        "##### :green-background[:green["
        f"{longest_streaks['Length'].iloc[0]} times in a row]]"
    )

""

# Streaks Timeline
st.write(f"### :yellow[{kind_2.capitalize()} Streaks Timeline]")
with st.container(border=True):
    fig: go.Figure
    fig = streaktimeline_interactive(sc_log, kind_2, year=year, minlength=10)
    fig.update_layout(paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF")
    st.plotly_chart(fig, theme=None)
