import typer
from typing import List, Literal
from typing_extensions import Annotated

from memoryfm.cli import(
    imports_file,
    import_data,
)
from memoryfm.cli.utils._loader_utils import (
    _load_saved_log,
    check_loaded,
)
from memoryfm.cli.utils._import_utils import get_imported_names
from memoryfm.cli.utils._cli_printer import cli_top_charts

app = typer.Typer(name="memory.fm")

app.add_typer(import_data.app, name="import")

@app.command("load")
def load(import_name: str):
    """Load imported ScrobbleLog"""
    _load_saved_log(import_name)

@app.command("list")
def list_imported():
    """List all imports"""
    import_names_list = get_imported_names(imports_file)
    print("Scrobble Logs:")
    print(import_names_list)

@app.command("loaded")
def loaded_name():
    """Show loaded ScrobbleLog"""
    import_name = check_loaded()
    print("Loaded import:", import_name)

@app.command("print")
def print_md(
    import_name: str = None,
    max_length: int = 10,
    meta: bool = False,
    from_date: str = None,
    to_date: str = None, 
    last: Annotated[
        str,
        typer.Option(
            help=(
                "Time period for the chart. Either (positive) integer number of days, or "
                "one of: week, month, year."
            )
        )
    ] = None,
    by_artists: List[str] = None,
    by_albums: List[str]= None,
    by_tracks: List[str] = None,
) -> None:
    """Print ScrobbleLog"""
    from memoryfm.cli.utils._cli_printer import print_scrobbles
    print_scrobbles(import_name, max_length, meta, from_date, to_date,
                    last, by_artists, by_albums, by_tracks)

@app.command("top")
def top_charts(
    kind: Literal['tracks', 'artists', 'albums'],
    import_name: str = None,
    n: int = 10,
    from_date: str = None,
    to_date: str = None, 
    last: Annotated[
        str,
        typer.Option(
            help=(
                "Time period for the chart. Either (positive) integer number of days, or "
                "one of: week, month, year."
            )
        )
    ] = None
) -> None:
    """
    Print top n tracks/artists/albums. Optionally filter by dates or timeperiod.
    """
    cli_top_charts(import_name, kind=kind, n=n, start=from_date,
                  end=to_date, last=last)


if __name__ == "__main__":
    app()
