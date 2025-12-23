from __future__ import annotations
from typing import TYPE_CHECKING
import streamlit as st

from memoryfm.streamlit.util import set_session_data
from memoryfm.streamlit.util import analytics_base_layout
from memoryfm.stats.attachment import weighted_attachment

if TYPE_CHECKING:
    from memoryfm import ScrobbleLog

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        padding-left: 3rem;
        padding-right: 3rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

page_name = "attachment_index"

# Page Layout
# --------------------------------------------------------------

# Header
st.title(":primary[:material/person_heart: Attachment Index]")
st.write("---")
st.info(
    "What is **Attachment Index**?\n\n"
    "**Attachment Index** is measure of how concentrated or your "
    "listening was on any given day.  \nA high **Attachment Index** indicates "
    "that your listening was focused on a small group of artists/albums/tracks.",
    icon=":material/info:",
)
""


# Update Session State
username = st.session_state["username"]
set_session_data(
    st.session_state["username"],
)
sc_log: ScrobbleLog
sc_log = st.session_state["sc_log"]

# Date Filter
data = analytics_base_layout(page_name, value="year")
dates = data["dates"]

# Select Chart Type
kind = data["kind"]
kind_2 = kind.rstrip("s")
attachment_index = weighted_attachment(sc_log, by=kind_2, freq="D")


# Attachment Index
# ---------------------------------------------------

attachment_index = weighted_attachment(sc_log, by=kind_2, freq="D", alpha=2)
attachment_index.index.name = "Timestamp"
attachment_index.name = "Attachment Index"
if dates["from_date"] and dates["to_date"]:
    date_filter = (attachment_index.index.date >= dates["from_date"]) & (
        attachment_index.index.date <= dates["to_date"]
    )
    filtered_att_index = attachment_index[date_filter]

else:
    filtered_att_index = attachment_index

filtered_att_index = filtered_att_index.round(2)

# Summary
# ----------------------------------------------
""
peak = filtered_att_index.max()
peak_index = filtered_att_index.index[filtered_att_index == peak]
peak_date = peak_index[0].strftime("%B %d, %Y")
st.write(
    "##### :red-background[:red[:material/calendar_today: "
    f"{kind_2.capitalize()} Attachment was highest on {peak_date}]]"
)
peak_sc_log = sc_log.filter_by_date(start=peak_index[0], end=peak_index[0])
scrobbles_count_peak = len(peak_sc_log)
top_charts_peak = peak_sc_log.top_charts(kind).head(1)
kind_peak = top_charts_peak.index[0]
scrobbles_kind_peak = top_charts_peak.values[0]
st.write(
    "##### :violet-background[:violet["
    f":material/trophy: Your Top {kind_2.capitalize()} that day was '{kind_peak}']]"
)
st.write(
    "##### :green-background[:green["
    ":material/pie_chart: With "
    f"{100 * scrobbles_kind_peak / scrobbles_count_peak:.0f}% "
    f"Scrobbles ({scrobbles_kind_peak}/{scrobbles_count_peak})]]"
)

# Attachment Index charts
# ------------------------------------------------------------
# Line chart
st.write(
    "##### :yellow-background[:yellow[:material/show_chart: "
    "Attachment Index throughout the period]]:"
)
""

st.line_chart(
    filtered_att_index.to_frame().reset_index(),
    x="Timestamp",
    y="Attachment Index",
)
