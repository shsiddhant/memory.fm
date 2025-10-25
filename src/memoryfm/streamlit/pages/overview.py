from __future__ import annotations
from typing import TYPE_CHECKING
import streamlit as st

from memoryfm.streamlit.util import set_session_data
from memoryfm.streamlit.pages.manage_imports import new_imports

new_imports_pg = st.Page(new_imports, title="New Import")


if TYPE_CHECKING:
    from memoryfm import ScrobbleLog

if "load_box" not in st.session_state:
    st.session_state.load_box = None


def overview():
    st.title("memory.fm")
    st.write("Manage your Last.fm scrobble data.")
    st.header("Load Your Data")
    username = st.selectbox(
        "Please select your username",
        st.session_state.imports,
        index=None,
        placeholder="username",
        key="load_box",
    )
    disabled_load = not username
    if st.button("Load import", disabled=disabled_load):
        set_session_data(username)
        st.success("Loaded succesfully")
    st.markdown(f"**Active import:** {st.session_state.get('username')}")
    st.info(
        "Click the ['New import'](new_imports) link above or from the left sidebar if"
        " you wish to add a new import."
    )
    if st.session_state.get("username") is not None:
        with st.container():
            st.header("Summary")
            st.markdown(summary(st.session_state["sc_log"]))


def summary(scrobble_log: ScrobbleLog) -> str:
    meta = scrobble_log.meta
    if meta["source"] == "spotify":
        listens = "num_listens"
        listens_key = "Listen"
    else:
        listens = "num_scrobbles"
        listens_key = "Scrobble"

    summary = f"""
**Username:** {meta["username"]}

**Timezone:** {meta["tz"]}

**Platform:** {meta["source"].capitalize()}

**{listens_key}s:** {meta[listens]}

**First {listens_key}:**

{scrobble_log[0:1]}

**Last {listens_key}:**

{scrobble_log[-1:].to_markdown(show_extra=False)}
    """
    return summary
