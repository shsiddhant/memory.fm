import typer
from typing import Literal, Optional
from typing_extensions import Annotated

from memoryfm._version import __version__
from memoryfm.cli import (
    import_data,
)
from memoryfm.cli.utils._loader_utils import (
    _load_saved_log,
)
from memoryfm.cli.utils._common_utils import (
    _normalise_username,
    check_loaded,
)
from memoryfm.cli.utils._import_utils import get_imported_names
from memoryfm.cli.utils._cli_printer import (
    cli_top_charts,
    print_scrobbles,
)


app = typer.Typer(name="memory.fm")

app.add_typer(import_data.app, name="import")


def version_callback(value: bool = False):
    """
    See version.
    """
    if value:
        print("memory.fm version", __version__)
        print("Copyright (c) 2025 Siddhant Sharma")
        print("Licensed under the MIT License")
        raise typer.Exit()


@app.callback()
def main(
    version: Annotated[
        Optional[bool], typer.Option("--version", callback=version_callback)
    ] = None,
):
    """
    Manage your music listening data from Last.fm or Spotify.

    Print, Filter, Analyse, Export

    ...and more
    """


@app.command("load")
def load(
    username: Annotated[str, typer.Argument(help="Load this username's scrobbles.")],
):
    """Load imported ScrobbleLog"""
    _load_saved_log(_normalise_username(username))


@app.command("list")
def list_imported():
    """List all imports"""
    import_names_list = get_imported_names()
    print("Scrobble Logs:")
    print(import_names_list)


@app.command("loaded")
def loaded_name():
    """Show loaded ScrobbleLog"""
    import_name = check_loaded()
    print("Loaded import:", import_name)


@app.command("print")
def print_md(
    username: Annotated[
        Optional[str],
        typer.Option(
            "--username", help=("Use this username log instead of the loaded one.")
        ),
    ] = None,
    maxm: Annotated[
        Optional[int],
        typer.Option("--max", help=("Maximum number of scrobbles to print.")),
    ] = 10,
    meta: Annotated[
        Optional[bool], typer.Option("--metadata", help=("Print metadata."))
    ] = False,
    from_date: Annotated[
        Optional[str],
        typer.Option("--from", help=("Filter scrobbles from this datetime.")),
    ] = None,
    to_date: Annotated[
        Optional[str],
        typer.Option("--to", help=("Filter scrobbles till this datetime.")),
    ] = None,
    last: Annotated[
        Optional[str],
        typer.Option(
            "--last",
            help=(
                "Time period to print the scrobbles. Either "
                "(positive) integer number of days, or one of: "
                "week, month, year."
            ),
        ),
    ] = None,
    by_artists: Annotated[
        Optional[list[str]],
        typer.Option("--artists", help=("Filter scrobbles by these artists.")),
    ] = None,
    by_albums: Annotated[
        Optional[list[str]],
        typer.Option("--albums", help=("Filter scrobbles by these albums.")),
    ] = None,
    by_tracks: Annotated[
        Optional[list[str]],
        typer.Option("--tracks", help=("Filter scrobbles by these tracks.")),
    ] = None,
) -> None:
    """Print ScrobbleLog."""
    print_scrobbles(
        _normalise_username(username),
        maxm,
        meta,
        from_date,
        to_date,
        last,
        by_artists,
        by_albums,
        by_tracks,
    )


@app.command("top")
def top_charts(
    kind: Literal["tracks", "artists", "albums"],
    username: Annotated[
        Optional[str],
        typer.Option(
            "--username", help=("Use this username instead of the loaded one.")
        ),
    ] = None,
    maxm: Annotated[
        Optional[int],
        typer.Option(
            "--max", help=("Maximum number of top tracks/artists/albums to show.")
        ),
    ] = 10,
    from_date: Annotated[
        Optional[str], typer.Option("--from", help=("Filter chart from this datetime."))
    ] = None,
    to_date: Annotated[
        Optional[str], typer.Option("--to", help=("Filter chart till this datetime."))
    ] = None,
    last: Annotated[
        Optional[str],
        typer.Option(
            "--last",
            help=(
                "Time period for the chart. Either (positive) integer "
                "number of days, or one of: week, month, year. "
                "Use this option only when --from and --to aren't used"
            ),
        ),
    ] = None,
) -> None:
    """
    Print top tracks/artists/albums. Optionally filter by dates or timeperiod.
    """
    cli_top_charts(
        _normalise_username(username),
        kind,
        maxm,
        start=from_date,
        end=to_date,
        last=last,
    )


if __name__ == "__main__":
    app()
