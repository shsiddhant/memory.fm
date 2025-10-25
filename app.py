from __future__ import annotations
import streamlit as st

from memoryfm.cli.utils._import_utils import get_imported_names
from memoryfm.streamlit.util import print_scrobbles, set_session_data
from memoryfm.streamlit.index import overview_pg, new_imports_pg, delete_import_pg

st.set_page_config(layout="wide")

if "imports" not in st.session_state:
    st.session_state.imports = get_imported_names()
if "delete" not in st.session_state:
    st.session_state.delete = None
if "deleted_user" not in st.session_state:
    st.session_state.deleted_user = None


def show_scrobbles():
    with st.container():
        cols = st.columns([1, 2])
        select_user = cols[0]
        with select_user:
            username = st.selectbox(
                "Select your username",
                st.session_state["imports"],
                index=None,
                placeholder="username",
            )
    with st.container(
        border=True,
    ):
        tog_print = st.toggle("Show scrobbles")
        st.write("View your scrobbles.")
        max_length = st.number_input(
            "Maximum number of scrobbles to show", value=10, min_value=0
        )
        if "date_range" not in st.session_state:
            st.session_state["Date Range"] = "All Time"
        with st.popover(
            st.session_state.get("date_range"), icon=":material/calendar_today:"
        ):
            from_date = st.date_input(
                label="From", value=st.session_state.get("from"), format="DD-MM-YYYY"
            )
            to_date = st.date_input(
                label="To", value=st.session_state.get("to"), format="DD-MM-YYYY"
            )
    set_session_data(username, max_length, from_date, to_date)
    if tog_print:
        st.session_state["print_button"] = 1
        print_scrobbles(username, max_length, from_date, to_date)


def load_import(username: str):
    st.write("### Load Import")
    try:
        set_session_data(username)
    except RuntimeError:
        st.error("Please select a username first.")
        st.stop()


pages = {
    "Overview": [overview_pg],
    "Manage Imports": [
        new_imports_pg,
        delete_import_pg,
    ],
}

pg = st.navigation(pages)
pg.run()
