import streamlit as st
from pathlib import Path

# pages = Path("pages/").resolve()
pages = Path(__file__).parent / "pages"
home = st.Page(
    page=pages / "home.py",
    title="Home",
    icon=":material/home:",
)
overview = st.Page(
    page=pages / "overview.py",
    title="Overview",
    icon=":material/list_alt:",
)
top_charts = st.Page(
    page=pages / "top_charts.py",
    title="Top Charts",
    icon=":material/bar_chart:",
)
attachment = st.Page(
    page=pages / "attachment.py",
    title="Attachment Index",
    icon=":material/person_heart:",
)
streaks = st.Page(
    page=pages / "streaks.py",
    title="Streaks",
    icon=":material/bolt:",
)

all_pages = [home, overview, top_charts, attachment, streaks]
