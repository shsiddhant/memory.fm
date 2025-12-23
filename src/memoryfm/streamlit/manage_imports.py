from __future__ import annotations
import streamlit as st
from io import TextIOWrapper
from typer import Exit
from requests import HTTPError

from memoryfm.cli.utils._import_utils import (
    import_and_save,
    get_imported_names,
    create_import_name_dir,
    write_import_files,
    add_to_imports,
)
from memoryfm.cli.utils._sync_utils import syncer
from memoryfm.cli import API_KEY
from memoryfm.streamlit.util import _delete_import


def source_formatting(text: str):
    return f"**{text.capitalize()}**"


def sync_with_api(username, api_key=API_KEY):
    if username in get_imported_names():
        info = f"Scrobbles for user {username} updated."
    else:
        info = f"New user added: {username}"
    scrobblesimport = st.progress(0, "Importing scrobbles ...")

    def statuscallback(
        page: int,
        totalpages: int,
        fetched_scrobbles: int,
        total_scrobbles: int,
        retry: int | None = None,
    ) -> None:
        pages_st = f":material/article: Page {page} of {totalpages}"
        scrobbles_st = (
            f":material/download: Imported {fetched_scrobbles} of "
            f"{total_scrobbles} scrobbles.\n"
        )
        statusstr = f"{pages_st}\n\n{scrobbles_st}"
        retrystr = f"Retry: {retry}"
        completed = 0.0
        string = ""
        if retry is not None and retry <= 5 and total_scrobbles:
            string = statusstr + retrystr
            completed = fetched_scrobbles / total_scrobbles
        elif retry is not None and retry <= 5:
            string = retrystr
        elif total_scrobbles:
            completed = fetched_scrobbles / total_scrobbles
            string = statusstr
        else:
            completed = 1.0
            string = ""
        if completed == 1.0:
            string = "Import finished."
        scrobblesimport.progress(value=completed, text=string)

    try:
        scrobble_log = syncer(username, api_key, statuscallback)
    except HTTPError as e:
        scrobble_log = None
        st.error(f"Error: {e.args[0]['message']}")
        st.stop()
    if scrobble_log is not None:
        import_name_dir = create_import_name_dir(username)
        write_import_files(username, scrobble_log)
        add_to_imports(username, overwrite=True)
        st.session_state.imports = get_imported_names()
        st.session_state["imports_source"] = dict.fromkeys(st.session_state["imports"])
        st.session_state["imports_source"][username] = "last.fm"
        succesful(info)
        return import_name_dir


def add_user():
    # Select source
    source = st.radio(
        "Select a source",
        options=["last.fm", "lastfmstats", "spotify"],
        key="source",
        format_func=source_formatting,
    )
    # Source: Last.fm (API call)
    if source == "last.fm":
        username = st.text_input(
            "**Last.fm username**",
            value=None,
            placeholder="Please enter your Last.fm username.",
        )
        submit = st.button("Import", key="sync_with_lastfm_api")
        if submit:
            import_name_dir = sync_with_api(username, API_KEY)
            return import_name_dir

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
    if source != "last.fm":
        overwrite = st.checkbox(
            "Overwrite", value=False, help="Overwrite if username already exists."
        )
    if source != "last.fm" and submit and file is not None:
        if source == "spotify" and not username:
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
            succesful(f"User was successfully added: {import_name_dir.name}")
            file_upload = None
            return import_name_dir
    elif source != "last.fm" and submit and file is None:
        st.error("Please upload a file first.")


@st.dialog("Successful !", on_dismiss="rerun")
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
