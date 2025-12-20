from __future__ import annotations
import streamlit as st
from typer import Exit

from memoryfm.cli.utils._import_utils import get_imported_names
from memoryfm.cli.utils._common_utils import check_loaded
from memoryfm.streamlit.util import print_scrobbles, set_session_data
from memoryfm.streamlit.index import all_pages, home

st.set_page_config(layout="wide")

if "imports" not in st.session_state:
    st.session_state.imports = get_imported_names()
if "delete" not in st.session_state:
    st.session_state.delete = None
if "deleted_user" not in st.session_state:
    st.session_state.deleted_user = None
if "username" not in st.session_state or st.session_state.username is None:
    try:
        st.session_state.username = check_loaded()
    except Exit:
        st.session_state.username = None
if st.session_state.username:
    set_session_data(st.session_state.username)


def show_scrobbles():
    username = st.session_state.username
    with st.container(
        border=True,
    ):
        tog_print = st.toggle("Show scrobbles")
        st.write("View your scrobbles.")
        max_length = st.number_input(
            "Maximum number of scrobbles to show", value=10, min_value=0
        )
        if "date_range" not in st.session_state:
            st.session_state["date_range"] = "All Time"
    dates = date_popover()
    set_session_data(username, max_length, *dates)
    if tog_print:
        st.session_state["print_button"] = 1
        print_scrobbles(username, max_length, *dates)


def date_popover():
    with st.popover(
        st.session_state.get("date_range"),
        icon=":material/calendar_today:",
    ):
        st.write("Select a date range")
        from_date = st.date_input(
            label="From",
            value=st.session_state.get("from"),
            format="DD-MM-YYYY",
        )
        to_date = st.date_input(
            label="To",
            value=st.session_state.get("to"),
            format="DD-MM-YYYY",
        )
        return from_date, to_date


if st.session_state.get("username"):
    scrobbles = st.Page(show_scrobbles, title="Scrobbles")
    pg = st.navigation(all_pages)
    pg.run()
else:
    pages = [
        home,
    ]
    pg = st.navigation(pages)
    pg.run()
