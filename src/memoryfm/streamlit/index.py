import streamlit as st
from pathlib import Path

pages = Path("src/memoryfm/streamlit/pages/").resolve()
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
