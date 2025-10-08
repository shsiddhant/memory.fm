from __future__ import annotations
import json
import typer
from memoryfm.cli import (
    base_dir,
    imports_dir,
    loaded_file,
    imports_file,
)
from memoryfm.cli.utils._import_utils import read_imports
from memoryfm import ScrobbleLog


def _load_saved_log(import_name: str):
    if not (imports_dir / f"{import_name}").exists():
        print(f"No ScrobbleLog with name: '{import_name}'")
        raise typer.Exit(2)
    imports_list = read_imports(imports_file)
    if import_name == "None":
        data = next(
                (d for d in imports_list if d.get("importname") is None),
                None
        )
    else:
        data = next(
                (d for d in imports_list if d.get("importname") == import_name),
                None
        )
    with open(loaded_file, 'w') as fp:
        json.dump(data, fp, indent=4)
    print("Loaded:", import_name)

def check_loaded(msg=None):
    try:
        with open(loaded_file, 'r') as fp:
            import_name = json.load(fp).get("importname")
    except FileNotFoundError:
        print("No import loaded.")
        raise typer.Exit(3)
    except json.JSONDecodeError:
        print("Loaded file invalid:", loaded_file)
    else:
        return import_name

def check_cache():
    if not base_dir.exists():
        raise FileNotFoundError(base_dir)


def read_cache_from_name(
    import_name: str = None,
    **kwargs
) -> ScrobbleLog:
    check_cache()
    import_name_dir = imports_dir / f"{import_name}"
    meta_file = import_name_dir / f'{import_name}-meta.json'
    df_file = import_name_dir / f'{import_name}-df.parquet'
    if not import_name_dir.exists():
        raise FileNotFoundError(import_name_dir)
    else:
        return ScrobbleLog.from_parquet(meta_file, df_file,
                                                 **kwargs)
