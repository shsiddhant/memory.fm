from __future__ import annotations

# from typing import TYPE_CHECKING
import streamlit as st

from memoryfm.streamlit.util import summary, set_session_data
from memoryfm.cli.utils._import_utils import get_imported_names


if "imports" not in st.session_state or st.session_state.imports is None:
    st.session_state["imports"] = get_imported_names()

if st.session_state.get("username") is not None:
    st.title("Overview")
    set_session_data(st.session_state.username)
    with st.container():
        st.subheader("Summary")
        st.markdown(summary(st.session_state["sc_log"]))
