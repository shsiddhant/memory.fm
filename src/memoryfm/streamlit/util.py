from __future__ import annotations
import streamlit as st
from io import TextIOWrapper
from typer import Exit
import json

from memoryfm.cli.utils._loader_utils import read_cache_from_name
from memoryfm.cli.utils._import_utils import import_and_save, read_imports
from memoryfm.cli.utils._common_utils import check_loaded
from memoryfm.cli import imports_dir, imports_file, loaded_file


def manage_imports():
    st.write("Manage your Lastfmstats/Spotify imports.")
    choice = st.radio(
        "Choose from the following.",
        options=["New import", "List imports", "Delete import"],
    )
    if choice == "New import":
        new_imports()
    elif choice == "List imports":
        st.write("List of all imports")
    elif choice == "Delete import":
        st.write("Delete an existing import")


def new_imports():
    st.write("### Import from lastfmstats/Spotify")
    source = st.selectbox(
        "Select a source", options=["Lastfmstats", "Spotify"], key="source"
    )
    file_upload = st.file_uploader("Upload the file", label_visibility="hidden")
    if source == "Lastfmstats" and file_upload is not None:
        file_type = st.radio("File Type", options=["json", "csv"])
        file = TextIOWrapper(file_upload, encoding="utf-8")
    elif source == "Spotify":
        file_type = None
        file = file_upload
    overwrite = st.checkbox("Overwrite existing import", value=False)
    username = st.text_input("Save with this username", value="None")
    import_but = st.button("Import")
    if import_but and file_upload is not None:
        try:
            import_and_save(file, file_type, source.lower(), overwrite, username)
        except Exit:
            st.error(
                "Username already exists. Please select overwrite if you wish"
                " to overwrite the existing import."
            )
        else:
            st.write("Imported and saved to", imports_dir / username)
    elif import_but and file_upload is None:
        st.error("Please upload a file first.")


def _delete_import(username: str):
    imports_list = read_imports()
    name_imported_data = next(
        (d for d in imports_list if d.get("importname") == username), None
    )
    imports_list.remove(name_imported_data)
    with open(imports_file, "w") as fp:
        json.dump(imports_list, fp, indent=4)
    meta_file = imports_dir / f"{username}" / f"{username}-meta.json"
    df_file = imports_dir / f"{username}" / f"{username}-df.parquet"
    meta_file.unlink()
    df_file.unlink()
    (imports_dir / f"{username}").rmdir()
    if loaded_file.is_file() and check_loaded() == username:
        loaded_file.unlink()


def set_session_data(
    username: str,
    max_length: int = 10,
    from_date: str | None = None,
    to_date: str | None = None,
) -> None:
    if username is not None:
        st.session_state["username"] = username
        st.session_state["max"] = max_length
        st.session_state["sc_log"] = read_cache_from_name(
            username, start=from_date, end=to_date
        )
        st.session_state["from"] = st.session_state["sc_log"].meta["date_range"][
            "start"
        ]
        st.session_state["to"] = st.session_state["sc_log"].meta["date_range"]["end"]
        if from_date is None and to_date is None:
            st.session_state["date_range"] = "All Time"
        else:
            st.session_state["date_range"] = (
                f"{st.session_state['from'].strftime('%d %b %Y')} to"
                f" {st.session_state['to'].strftime('%d %b %Y')}"
            )
        st.session_state["meta"] = st.session_state["sc_log"].meta
    else:
        raise RuntimeError


def print_scrobbles(
    username: str,
    max_length: int = 10,
    from_date: str | None = None,
    to_date: str | None = None,
) -> None:
    try:
        set_session_data(username, max_length, from_date, to_date)
    except RuntimeError:
        st.error("Please select a username first.")
        st.stop()
    else:
        st.dataframe(
            st.session_state["sc_log"].head(max_length).df,
            row_height=70,
            hide_index=True,
        )
