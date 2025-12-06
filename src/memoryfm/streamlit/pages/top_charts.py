from __future__ import annotations
from typing import TYPE_CHECKING
import streamlit as st

from memoryfm.cli.utils._cli_printer import date_filter
from memoryfm.streamlit.util import set_session_data
import plotly.express as px

if TYPE_CHECKING:
    from typing import Literal
    from memoryfm import ScrobbleLog

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

if "filter_kwargs" not in st.session_state:
    st.session_state["filter_kwargs"] = {
        "artists": None,
        "albums": None,
        "tracks": None,
    }
if "filter_values" not in st.session_state:
    st.session_state["filter_values"] = []

# Format Header
# -----------------------------------------------------------------------
icons = {"artists": "artist", "albums": "album", "tracks": "music_note"}
colors = {"artists": "blue", "albums": "green", "tracks": "orange"}
filters_allowed = {
    "artists": None,
    "albums": ["artists"],
    "tracks": ["artists", "albums"],
}


def format_chart_type(text: Literal["artists", "albums", "tracks"]):
    return f":material/{icons[text]}: {text.capitalize()}"


# Time Periods
# ---------------------------------------------------------------------------
def time_periods():
    st.markdown("#### :material/calendar_today: Time Period")
    time_period = st.radio(
        "Time period",
        options=["week", "month", "year", "all time", "custom date range"],
        horizontal=True,
        label_visibility="hidden",
        format_func=str.title,
    )
    if time_period in ["week", "month", "year"]:
        from_date, to_date = date_filter(last=time_period)
    elif time_period == "all time":
        from_date, to_date = None, None
    elif time_period == "custom date range":
        from_date_col, to_date_col = st.columns([1, 1])
        with from_date_col:
            from_date = st.date_input(
                label="**From**",
                value=st.session_state.get("from"),
                format="DD-MM-YYYY",
            )
        with to_date_col:
            to_date = st.date_input(
                label="**To**",
                value=st.session_state.get("to"),
                format="DD-MM-YYYY",
            )
    return from_date, to_date


# Top 5 Bar Chart
# ------------------------------------------------------------------------------
def bar_chart(
    sc_log: ScrobbleLog, kind: str, max_bars: int = 5, color: str = "#B40B08"
):
    ser = sc_log.top_charts(kind).head(max_bars)
    fig = px.bar(
        x=ser.values,
        y=ser.index,
        color=ser.index,
        height=300,
        width=800,
        labels={"color": ser.index.name},
    )
    fig.update_yaxes(
        showticklabels=False,
        title=ser.index.name,
        categoryorder="total ascending",
    )
    fig.update_xaxes(
        title=ser.name,
    )
    st.plotly_chart(fig)


# Filters
# -------------------------------------------------------------------------------
filters_allowed = {
    "artists": None,
    "albums": ["artists"],
    "tracks": ["artists", "albums"],
}


def show_filters():
    st.markdown("##### :material/filter_list: Filter By")
    filter_type = st.radio(
        "Filter Type",
        options=filters_allowed[kind],
        format_func=format_chart_type,
        horizontal=True,
        label_visibility="collapsed",
    )
    if filter_type:
        filter_values = st.multiselect(
            "Filter by",
            options=sorted(sc_log.df.loc[:, filter_type.rstrip("s")].dropna().unique()),
            placeholder=f"Search {filter_type}",
            label_visibility="collapsed",
        )
    else:
        filter_values = None
    if filter_values and len(filter_values):
        st.session_state["filter_kwargs"] = {filter_type: filter_values}
    else:
        st.session_state["filter_kwargs"] = {
            "artists": None,
            "albums": None,
            "tracks": None,
        }


# Page Layout
# ----------------------------------------------------------------

# Header
# ------------------------------------------------------
st.title(":primary[:material/bar_chart: Top Charts]")
st.write("---")
st.markdown(f"### :material/person: {st.session_state.username}")
""

# Date Range
if "date_range" not in st.session_state:
    st.session_state["date_range"] = "All Time"

with st.container():
    kind_col, dates_col = st.columns([3, 3], border=True)
with dates_col:
    from_date, to_date = time_periods()

# Update Session State
dates = {"from_date": from_date, "to_date": to_date}
username = st.session_state["username"]
set_session_data(st.session_state["username"], **dates)
sc_log = st.session_state["sc_log"]

# Select Chart Type
with kind_col:
    st.markdown("#### :material/view_list: Chart Type")
    kind = st.radio(
        "Pick a chart type",
        ["artists", "albums", "tracks"],
        horizontal=True,
        format_func=format_chart_type,
    )
""
""

# Subheader
st.subheader(f":material/{icons[kind]}: Your Top {kind.capitalize()}")

# Bar Chart
if sc_log:
    ser = sc_log.top_charts(kind)
    st.write("")
    st.write("")
    with st.container(border=True):
        bar_chart(sc_log, kind)

# Tabular Chart
with st.container(border=False):
    filters, max_length_col = st.columns(
        [1, 1],
        gap="large",
        vertical_alignment="top",
    )
    with max_length_col:
        st.write(f"##### {kind.capitalize()} to show")
        max_l = st.slider(
            "Max",
            min_value=0,
            max_value=50,
            label_visibility="hidden",
            value=10,
            step=5,
        )
    with filters:
        show_filters()
    set_session_data(
        st.session_state["username"], **dates, **st.session_state["filter_kwargs"]
    )
    sc_log = st.session_state["sc_log"]
    if sc_log:
        ""
        ser = sc_log.top_charts(kind)
if sc_log:
    st.write(ser.head(max_l).to_markdown())
else:
    st.info("No scrobbles found within the specified date range.")
