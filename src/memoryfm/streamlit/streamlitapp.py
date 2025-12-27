from __future__ import annotations
import streamlit as st
from typer import Exit
import json

from memoryfm.cli import imports_dir
from memoryfm.cli.utils._import_utils import get_imported_names
from memoryfm.cli.utils._common_utils import check_loaded
from memoryfm.streamlit.util import set_session_data
from memoryfm.streamlit.index import all_pages, home

st.set_page_config(layout="wide")

if "imports" not in st.session_state:
    st.session_state.imports = get_imported_names()
    st.session_state.imports.sort()
if "imports_source" not in st.session_state:
    st.session_state["imports_source"] = dict.fromkeys(st.session_state["imports"])
    for username in st.session_state["imports"]:
        with open(imports_dir / username / f"{username}-meta.json", "r") as fp:
            st.session_state["imports_source"][username] = json.load(fp)["source"]
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


if st.session_state.get("username"):
    pg = st.navigation(all_pages)
    pg.run()
else:
    pages = [
        home,
    ]
    pg = st.navigation(pages)
    pg.run()
