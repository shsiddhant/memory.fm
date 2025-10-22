from __future__ import annotations
from typing import Optional
from typing_extensions import (
    Annotated,
    Literal,
)
import typer
from pathlib import Path  # noqa: TC003

from memoryfm.cli.utils._import_utils import (
    import_and_save,
    _delete_saved_import,
)
from memoryfm.cli.utils._common_utils import _normalise_username

app = typer.Typer()


@app.callback()
def callback():
    """
    Import scrobbles from lastfmstats exports or spotify listening history data
    """


@app.command("lastfmstats")
def import_lastfmstats(
    file: Path, file_type: Literal["json", "csv"] = "json", overwrite: bool = False
) -> None:
    """
    Import JSON/CSV export obtained from lastfmstats.com
    """
    import_and_save(file, file_type, "lastfmstats", overwrite=overwrite)


@app.command("spotify")
def import_spotify(
    file: Path,
    username: Annotated[Optional[str], typer.Option()] = None,
    overwrite: bool = False,
    min_dur: Annotated[
        int,
        typer.Option(help="Minimum duration below which the scrobbles are discarded"),
    ] = 60,
) -> None:
    """
    Import Spotify Listening History zip or JSON.
    """
    import_and_save(
        file,
        file_type="json",
        source="spotify",
        import_name=_normalise_username(username),
        overwrite=overwrite,
        min_duration_seconds=min_dur,
    )


@app.command("delete")
def delete(username: str, confirm: bool = True):
    """
    Delete an existing import
    """
    _delete_saved_import(_normalise_username(username), confirm=confirm)


if __name__ == "__main__":
    app()
