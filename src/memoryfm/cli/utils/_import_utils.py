from __future__ import annotations
import json
import zipfile
from typing import TYPE_CHECKING, Literal
from typer import Exit
from memoryfm.io.lastfmstats import from_lastfmstats
from memoryfm.io.spotify import (
    from_spotify,
    from_spotify_zip,
)
from memoryfm.io._writers import _write_string
from memoryfm.errors import InvalidDataError
from memoryfm.cli import base_dir, imports_dir, imports_file, loaded_file

if TYPE_CHECKING:
    from pathlib import Path
    from memoryfm import ScrobbleLog


def create_import_name_dir(name: str | None) -> Path:
    import_name_dir = imports_dir / f"{name}"
    import_name_dir.mkdir(parents=True, exist_ok=True)
    return import_name_dir


def write_import_files(name: str | None, scrobble_log: ScrobbleLog) -> None:
    import_name_dir = create_import_name_dir(name)
    meta_file = import_name_dir / f"{name}-meta.json"
    df_file = import_name_dir / f"{name}-df.parquet"
    scrobble_log.to_parquet(meta_file, df_file)


from datetime import datetime


def add_to_imports(name: str | None, overwrite: bool = False):
    try:
        imports_data = read_imports(check_exist=False)
        validate_imports_file(imports_data)
    except (FileNotFoundError, json.JSONDecodeError, InvalidDataError):
        imports_data = []
    names = get_imported_names()
    if name in names and not overwrite:
        print(
            f"Scrobble Log with the name {name} already exists."
            "Try --overwrite to overwrite the existing import"
        )
        raise Exit(3)
    elif name in names and overwrite:
        name_imported_data = next(
            (d for d in imports_data if d.get("importname") == name), None
        )
        imports_data.remove(name_imported_data)
    imported_data = {
        "importname": name,
        "importdate": datetime.now().isoformat(),
        "path": f"{base_dir}/imports/{name}",
    }
    imports_data.append(imported_data)
    _write_string(json.dumps(imports_data, indent=4), file=imports_file)


from memoryfm.cli.utils._common_utils import check_loaded


def _delete_saved_import(import_name: str | None, confirm=True):
    names = get_imported_names()
    if import_name not in names:
        print("No import found for import name:", import_name)
        raise Exit(2)
    elif confirm:
        confirmation = input(
            f"Are you sure you want to delete import {import_name}? (y/N):"
        )
    if confirmation == "y":
        imports_list = read_imports()
        name_imported_data = next(
            (d for d in imports_list if d.get("importname") == import_name), None
        )
        imports_list.remove(name_imported_data)
        with open(imports_file, "w") as fp:
            json.dump(imports_list, fp, indent=4)
        meta_file = imports_dir / f"{import_name}" / f"{import_name}-meta.json"
        df_file = imports_dir / f"{import_name}" / f"{import_name}-df.parquet"
        meta_file.unlink()
        df_file.unlink()
        (imports_dir / f"{import_name}").rmdir()
        if loaded_file.is_file() and check_loaded() == import_name:
            loaded_file.unlink()
        print("Import deleted:", import_name)


def import_and_save(
    file: Path,
    file_type: Literal["json", "csv"],
    source: Literal["lastfmstats", "spotify"],
    overwrite: bool,
    import_name: str | None = None,
    min_duration_seconds: int = 60,
) -> None:
    """
    Import Last.fm scrobble data or Spotify Listening History.
    """
    ensure_files_and_dirs()
    scrobble_log = None
    if source == "lastfmstats":
        scrobble_log = from_lastfmstats(file, file_type)
        if import_name is None and scrobble_log.meta.get("username") is not None:
            import_name = scrobble_log.meta.get("username")
    elif source == "spotify" and zipfile.is_zipfile(file):
        scrobble_log = from_spotify_zip(
            file, username=import_name, min_duration_ms=min_duration_seconds * 1000
        )
    elif source == "spotify" and not zipfile.is_zipfile(file):
        scrobble_log = from_spotify(
            file, username=import_name, min_duration_ms=min_duration_seconds * 1000
        )
    else:
        print("No such source available:", source)
    if import_name in get_imported_names() and not overwrite:
        print(
            f"Scrobble Log with the name {import_name} already exists."
            "Try --overwrite to overwrite the existing import"
        )
        raise Exit(3)
    if scrobble_log is not None:
        import_name_dir = create_import_name_dir(import_name)
        write_import_files(import_name, scrobble_log)
        add_to_imports(import_name, overwrite=overwrite)
        print("Imported and saved to", import_name_dir)


def read_imports(check_exist=True) -> list:
    if check_exist:
        ensure_files_and_dirs()
    try:
        with open(imports_file, "r") as fp:
            data = json.load(fp)
    except json.JSONDecodeError:
        print("No imports found, imports file is invalid:", imports_file)
        ensure_files_and_dirs()
        return []

    else:
        return validate_imports_file(data)


def validate_imports_file(data) -> list:
    if not isinstance(data, list):
        print("No imports found")
        return []
    else:
        return data


def get_imported_names() -> list:
    data = read_imports()
    names = [d.get("importname") for d in data]
    return names


def ensure_files_and_dirs() -> None:
    imports_dir.mkdir(exist_ok=True)
    if not imports_file.is_file():
        imports_file.write_text("[\n]")
