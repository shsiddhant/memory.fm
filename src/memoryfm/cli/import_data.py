from __future__ import annotations 
from typing import Literal
import typer
from pathlib import Path
from memoryfm.cli.utils._import_utils import import_and_save, _delete_saved_import 


app = typer.Typer()

@app.callback()
def callback():
    """
    Import scrobbles from lastfmstats exports or spotify listening history data
    """

@app.command("lastfmstats")
def import_lastfmstats(
    file: Path,
    file_type: Literal['json', 'csv'] = 'json',
    overwrite: bool = False
) -> None:
    """
    Import JSON/CSV export obtained from lastfmstats.com
    """
    import_and_save(file, file_type, "lastfmstats", overwrite=overwrite)

@app.command("spotify")
def import_spotify(
    file: Path,
    username: str = None,
    overwrite: bool = False,
    min_duration_seconds: int = 60,
) -> None:
    """
    Import Spotify Listening History zip or JSON.
    """
    import_and_save(file, file_type="json", source="spotify",
                    import_name=username, overwrite=overwrite,
                    min_duration_seconds=min_duration_seconds)

@app.command("delete")
def delete(import_name: str, confirm: bool = True):
    """
    Delete an existing import
    """
    _delete_saved_import(import_name, confirm=confirm)


if __name__ == "__main__":
    app()
