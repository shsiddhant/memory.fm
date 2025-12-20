from __future__ import annotations
import streamlit as st

from memoryfm.streamlit.util import set_session_data


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

page_name = "attachment_index"

# Page Layout
# --------------------------------------------------------------

# Header
st.title(":primary[:material/person_heart: Attachment Index]")
st.write("---")
st.markdown(f"### :material/person: {st.session_state.username}")
""


from memoryfm.streamlit.util import analytics_base_layout

# Update Session State
data = analytics_base_layout(page_name)
dates = data["dates"]
username = st.session_state["username"]
set_session_data(st.session_state["username"], **dates)
sc_log = st.session_state["sc_log"]

# Select Chart Type
kind = data["kind"]

# Attachment Index charts
# ------------------------------------------------------------

# Line chart

from memoryfm.viz.attachment import weighted_attachment_plot


# Rolling average chart
fig = weighted_attachment_plot(sc_log, kind.rstrip("s"))
st.plotly_chart(fig)
