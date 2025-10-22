import json
import typer

from memoryfm.cli import loaded_file


def _normalise_username(username: str | None) -> str | None:
    """If username is "None", return ``None``, else return username"""
    if username == "None":
        return None
    else:
        return username


def check_loaded(msg=None):
    try:
        with open(loaded_file, "r") as fp:
            import_name = json.load(fp).get("importname")
    except FileNotFoundError:
        print("No import loaded.")
        raise typer.Exit(3)
    except json.JSONDecodeError:
        print("Loaded file invalid:", loaded_file)
    else:
        return import_name
