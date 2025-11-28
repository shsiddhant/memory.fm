from __future__ import annotations
from rich.progress import Progress
from memoryfm.cli.utils._import_utils import (
    get_imported_names,
    create_import_name_dir,
    write_import_files,
    add_to_imports,
)
from typing import TYPE_CHECKING
from typer import Exit
from requests import HTTPError
from memoryfm.cli.utils._loader_utils import read_cache_from_name
from memoryfm.io._normalise import normalise_lastfmstats
from memoryfm.io.lastfm_api import (
    df_from_timestamp,
    from_lastfm_api,
)
from memoryfm import ScrobbleLog

if TYPE_CHECKING:
    from collections.abc import Callable


def sync_import_with_api(username: str, api_key: str):
    try:
        with Progress() as progress:
            scrobblesimport = progress.add_task("Importing scrobbles ...", total=1)

            def statuscallback(
                page: int,
                totalpages: int,
                fetched_scrobbles: int,
                total_scrobbles: int,
                retry: int | None = None,
            ) -> None:
                statusstr = (
                    f"Page {page} of {totalpages}\n"
                    f"Imported {fetched_scrobbles} of {total_scrobbles} scrobbles.\n"
                )
                retrystr = f"Retry: {retry}"
                completed = 0
                string = ""
                if retry is not None and retry <= 5 and total_scrobbles:
                    string = statusstr + retrystr
                    completed = fetched_scrobbles / total_scrobbles
                elif retry is not None and retry <= 5:
                    string = retrystr
                elif total_scrobbles:
                    string = statusstr
                    completed = fetched_scrobbles / total_scrobbles
                else:
                    completed = 1
                    string = ""
                progress.update(
                    scrobblesimport, completed=completed, description=string
                )

            scrobble_log = syncer(
                username,
                api_key,
                statuscallback,
            )
    except HTTPError as e:
        scrobble_log = None
        print("Error:", e.args[0]["message"])
        raise Exit(e.args[0]["error"])
    if scrobble_log is not None:
        import_name_dir = create_import_name_dir(username)
        write_import_files(username, scrobble_log)
        add_to_imports(username, overwrite=True)
        print("Imported and saved to", import_name_dir)
        return import_name_dir


def syncer(
    username: str,
    api_key: str,
    statuscallback: Callable[[int, int, int, int], None] | None = None,
):
    if username not in get_imported_names():
        scrobble_log = from_lastfm_api(
            username,
            api_key,
            statuscallback=statuscallback,
        )
    else:
        scrobble_log = read_cache_from_name(username)
        timestamp = scrobble_log.df["timestamp"].max()
        df_recent = df_from_timestamp(
            username,
            api_key,
            timestamp,
            statuscallback=statuscallback,
        )
        df_recent.dropna(axis=1, how="all")
        if not df_recent.empty:
            scrobble_log_recent = normalise_lastfmstats(df_recent, username, unit="s")
            scrobble_log.append(scrobble_log_recent)
            scrobble_log = ScrobbleLog(
                df=scrobble_log.df.drop_duplicates(ignore_index=True),
                username=username,
                tz=scrobble_log.tz,
                source="last.fm",
            )
    return scrobble_log
