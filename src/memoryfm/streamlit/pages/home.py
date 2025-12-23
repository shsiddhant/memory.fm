from __future__ import annotations
import streamlit as st
import json
from memoryfm.cli import imports_dir

from memoryfm.cli.utils._import_utils import get_imported_names
from memoryfm.streamlit.util import set_session_data
from memoryfm.streamlit.manage_imports import add_user, confirm_delete, sync_with_api
from memoryfm.streamlit.index import overview

if "imports" not in st.session_state or st.session_state.imports is None:
    st.session_state["imports"] = get_imported_names()
    st.session_state.imports.sort()

if "imports_source" not in st.session_state:
    st.session_state["imports_source"] = dict.fromkeys(st.session_state["imports"])
for username in st.session_state["imports"]:
    with open(imports_dir / username / f"{username}-meta.json", "r") as fp:
        st.session_state["imports_source"][username] = json.load(fp)["source"]


def users_list():
    st.session_state.imports.sort()
    for username in st.session_state.imports:
        with st.container():
            user, modify = st.columns([1, 1])
            with modify:
                sync, delete = st.columns([1, 5])
        with user:
            if st.button(
                f"**:material/person: {username}**",
                help="Load user",
            ):
                with st.spinner(
                    text="Loading your data...",
                ):
                    set_session_data(username)
                    st.switch_page(overview)
        with sync:
            sync_scrobbles = False
            if st.session_state["imports_source"][username] == "last.fm":
                if st.button(
                    "**:green[:material/sync:]**",
                    key=f"sync {username}",
                    type="tertiary",
                    help="Sync scrobbles",
                ):
                    sync_scrobbles = True
        with delete:
            if st.button(
                ":primary[:material/delete:]",
                key=f"delete {username}",
                type="tertiary",
                help="Delete user",
            ):
                confirm_delete(username)
        if st.session_state.deleted_user:
            st.session_state.deleted_user = None
        if sync_scrobbles:
            sync_with_api(username)


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

# Header
st.title(":red[memory.fm]")
"##### *music meets memory*"
"---"

userslist, adduser = st.columns(2)
# Users list
with userslist:
    st.header(":material/library_music: Your Music")
    st.markdown("### :material/groups: Users")
    if st.session_state.imports:
        "\n"
        users_list()
    else:
        st.write("**No users found**")
# Add new user
with adduser:
    st.header(":material/person_add: New User", help="Add new user")
    st.write("### :material/download: Import from Last.fm/lastfmstats/Spotify")
    add_user()
