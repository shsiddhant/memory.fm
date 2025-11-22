from __future__ import annotations
import streamlit as st
from io import TextIOWrapper
from typer import Exit

from memoryfm.cli.utils._import_utils import import_and_save, get_imported_names
from memoryfm.streamlit.util import _delete_import


def source_formatting(text: str):
    return f"**{text.capitalize()}**"


def add_user():
    # Select source
    source = st.radio(
        "Select a source",
        options=["lastfmstats", "spotify"],
        key="source",
        format_func=source_formatting,
    )
    # File Type
    # Source: Lastfmstats
    if source == "lastfmstats":
        file_type = st.radio("File Type", options=["json", "csv"])
        with st.form("file_uploader", clear_on_submit=True):
            file_upload = st.file_uploader(
                "Upload the file", label_visibility="hidden", type=file_type
            )
            submit = st.form_submit_button("Import")
        if file_upload is not None:
            file = TextIOWrapper(file_upload, encoding="utf-8")
        username = None
    # Source: Spotify
    elif source == "spotify":
        with st.form("file_uploader", clear_on_submit=True):
            file_upload = st.file_uploader(
                "Upload the file",
                label_visibility="hidden",
                type="zip",
            )
            submit = st.form_submit_button("Import")
        file_type = None
        file = file_upload
        # username is mandatory when source is spotify.
        username = st.text_input(
            "**Username**", value=None, placeholder="Please enter a username."
        )
    # Overwrite if username already exists.
    overwrite = st.checkbox(
        "Overwrite", value=False, help="Overwrite if username already exists."
    )
    if submit and file is not None:
        if not username:
            st.error("Username cannot be blank")
            st.stop()
        try:
            import_name_dir = import_and_save(
                file, file_type, source, overwrite, username
            )
        except Exit:
            st.error(
                "User already exists. Please select 'Overwrite' if you wish"
                " to overwrite the existing user."
            )
        else:
            st.session_state.imports = get_imported_names()
            succesful(f"User '{username}' was successfully added..")
            file_upload = None
            return import_name_dir
    elif submit and file is None:
        st.error("Please upload a file first.")


@st.dialog("Import Successful.", on_dismiss="rerun")
def succesful(message: str):
    st.success(message, icon=":material/task_alt:")


@st.dialog("Delete import")
def confirm_delete(username: str) -> bool:
    st.write(f"Are you sure you want to delete import: {username}?")
    yes, no = st.columns(2)
    if yes.button("Yes", icon=":material/check_circle:"):
        _delete_import(username)
        # Refresh imports list session state
        st.session_state.imports = get_imported_names()
        # Reset username
        st.session_state.username = None
        st.rerun()
    elif no.button("No", icon=":material/cancel:"):
        st.rerun()
