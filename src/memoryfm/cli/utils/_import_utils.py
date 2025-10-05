from __future__ import annotations
from pathlib import Path
import memoryfm
import json
from typing import Literal
from memoryfm.io.lastfmstats import from_lastfmstats
from memoryfm.io.spotify import from_spotify
from memoryfm.io._writers import _write_string
from memoryfm.errors import InvalidDataError
from memoryfm.cli import (
    base_dir,
    imports_dir,
    imports_file,
    loaded_file
)


def create_import_name_dir(name: str) -> Path:
    import_name_dir = imports_dir / name
    import_name_dir.mkdir(parents=True, exist_ok=True)
    return import_name_dir

def write_import_files(
    name: str,
    scrobble_log: memoryfm.ScrobbleLog
) -> None:
    import_name_dir = create_import_name_dir(name)
    meta_file = import_name_dir / f'{name}-meta.json'
    df_file = import_name_dir / f'{name}-df.parquet'
    scrobble_log.to_parquet(meta_file, df_file)

def add_to_imports(name: str, overwrite: bool = False):
    try:
        imports_data = read_imports(imports_file, check_exist=False)
        validate_imports_file(imports_data)
    except (
        FileNotFoundError,
        json.JSONDecodeError,
        InvalidDataError
    ):
        imports_data = []
    names = [d.get('import-name') for d in imports_data]
    if name in names and not overwrite:
        raise InvalidDataError(
                f"Scrobble Log with the name {name} already exists."
                "Try --overwrite to overwrite the existing import"
        )
    elif name not in names:
        from datetime import datetime
        imported_data = {   
                            "importname": name,
                            "importdate": datetime.now().isoformat(),
                            "path": f"{base_dir}/imports/{name}"
        }
        imports_data.append(imported_data)
    _write_string(json.dumps(imports_data, indent=4), file=imports_file)

def _delete_saved_import(import_name: str, confirm=True):
    names = get_imported_names(imports_file)
    if import_name not in names:
        print("No import found for import name:", import_name)
        from typer import Exit
        raise Exit(2)
    elif confirm:
       confirmation = input(
           f"Are you sure you want to delete import {import_name}? (Y/n):")
       confirmation = check_confirmation_input(confirmation)
    if confirmation == 'Y':
        imports_list = read_imports(imports_file)
        name_imported_data = next(
            (d for d in imports_list if d.get("importname") == import_name),
            None)
        imports_list.remove(name_imported_data)
        with open(imports_file, 'w') as fp:
            json.dump(imports_list, fp, indent=4)
        meta_file = imports_dir / import_name / f"{import_name}-meta.json"
        df_file = imports_dir / import_name / f"{import_name}-df.parquet"
        meta_file.unlink()
        df_file.unlink()
        (imports_dir / import_name).rmdir()
        from ._loader_utils import check_loaded
        if loaded_file.is_file() and check_loaded() == import_name:
            loaded_file.unlink()
        print("Import deleted:", import_name) 
    
def check_confirmation_input(confirmation) -> str:
    if confirmation not in ['Y', 'n']:
        confirmation = input("Please enter (Y/n): ")
        check_confirmation_input(confirmation)
    else:
        return confirmation
    
def import_and_save(
    file: Path,
    file_type: Literal["json", "csv"],
    source: Literal["lastfmstats", "spotify"],
    overwrite: bool,
    import_name: str | None = None,
) -> None:
    scrobble_log = None
    if source == "lastfmstats":
        scrobble_log = from_lastfmstats(file, file_type)
        if (
            import_name == "default" and
            scrobble_log.meta.get("username") is not None
        ):
            import_name = scrobble_log.meta.get("username")
    elif source == "spotify":
        scrobble_log = from_spotify(file, username=import_name)
    else:
        print("No such source available:", source)
    if scrobble_log is not None:
        import_name_dir = create_import_name_dir(import_name)
        write_import_files(import_name, scrobble_log)
        add_to_imports(import_name, overwrite=overwrite)
        print("Imported and saved to", import_name_dir)

def imports_file_exists(imports_file: Path) -> None:
    if not imports_file.exists():
        print("No imports found.")
        import typer
        raise typer.Exit(1)

def read_imports(imports_file: Path, check_exist=True) -> list | None:
    if check_exist:
        imports_file_exists(imports_file)
    try:
        with open(imports_file, 'r') as fp:
            data = json.load(fp)
    except json.JSONDecodeError:
        print("Imports file is invalid:", imports_file)
    else:
        return validate_imports_file(data)

def validate_imports_file(data):
    if not isinstance(data, list):
        raise InvalidDataError("Imports file is invalid:", imports_file)
    else:
        return data

def get_imported_names(imports_file: Path) -> list:
    data = read_imports(imports_file)
    names = [d.get("importname") for d in data]
    return names
