from __future__ import annotations
import streamlit as st
from io import TextIOWrapper
from typer import Exit

from memoryfm.cli.utils._import_utils import import_and_save, get_imported_names
from memoryfm.streamlit.util import _delete_import


def new_imports():
    st.title("Import from lastfmstats/Spotify")
    source = st.radio(
        "Select a source", options=["Lastfmstats", "Spotify"], key="source"
    )
    file_upload = st.file_uploader("Upload the file", label_visibility="hidden")
    if source == "Lastfmstats" and file_upload is not None:
        file_type = st.radio("File Type", options=["json", "csv"])
        file = TextIOWrapper(file_upload, encoding="utf-8")
        username = None
    elif source == "Spotify":
        file_type = None
        file = file_upload
        username = st.text_input("Save with this username", value="None")
    overwrite = st.checkbox("Overwrite existing import", value=False)
    import_but = st.button("Import")
    if import_but and file_upload is not None:
        try:
            import_name_dir = import_and_save(
                file, file_type, source.lower(), overwrite, username
            )
        except Exit:
            st.error(
                "Username already exists. Please select overwrite if you wish"
                " to overwrite the existing import."
            )
        else:
            st.write("Imported and saved to", import_name_dir)
            st.session_state.imports = get_imported_names()
    elif import_but and file_upload is None:
        st.error("Please upload a file first.")


def list_imports():
    pass


@st.dialog("Delete import")
def confirm_delete(username: str) -> bool:
    if "delete" not in st.session_state:
        st.session_state["delete"] = None
    st.write(f"Are you sure you want to delete import: {username}?")
    yes, no = st.columns(2)
    if yes.button("Yes", icon=":material/check_circle:"):
        _delete_import(username)
        st.session_state.deleted_user = username
        st.session_state.imports = get_imported_names()
        st.session_state.username = None
        st.rerun()
    elif no.button("No", icon=":material/cancel:"):
        st.rerun()


def delete_import():
    st.title("Delete an existing import.")
    username = st.selectbox(
        "Please select a username",
        st.session_state.imports,
        index=None,
        placeholder="username",
        key="delete_box",
    )
    disabled = not username
    if st.button("Delete import", disabled=disabled):
        confirm_delete(username)
    if st.session_state.deleted_user:
        st.write(f"Import for user {st.session_state.deleted_user} deleted.")
        st.session_state.deleted_user = None
