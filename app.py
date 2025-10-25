from __future__ import annotations
import streamlit as st

from memoryfm.cli.utils._import_utils import get_imported_names
from memoryfm.streamlit.util import print_scrobbles, manage_imports, set_session_data

if "imports" not in st.session_state:
    st.session_state["imports"] = get_imported_names()


def overview():
    with st.container():
        st.title("memory.fm")
        st.write("Manage your Last.fm scrobble data.")

    username = st.selectbox(
        "Please select your username",
        st.session_state["imports"],
        index=None,
        placeholder="username",
    )
    if st.button("Load import"):
        set_session_data(username)
    st.write("**Loaded import:**", st.session_state.get("username"))
    if st.session_state.get("username") is not None:
        st.json(body=st.session_state["meta"])


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


pg = st.navigation(
    [
        st.Page(overview, title="Overview"),
        st.Page(manage_imports, title="Manage Imports"),
    ]
)
pg.run()
# with st.sidebar:
#    st.write("## Welcome to memory.fm")
#    sidebar_option = st.radio(label = "", options = ["Manage Imports", "Load Import"])
# if sidebar_option == "Manage Imports":
#    manage_imports()
# elif sidebar_option == "Load Import":
#    load_import()
# else:
#    st.write("Placeholder")
