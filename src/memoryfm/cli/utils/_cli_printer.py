from __future__ import annotations
from typing import TYPE_CHECKING
from memoryfm.cli.utils._loader_utils import read_cache_from_name
from datetime import datetime, timedelta
from typer import Exit

if TYPE_CHECKING:
    from typing import Any


def date_filter(**kwargs) -> tuple[Any | None, Any | None]:
    literals = {"week": 7, "month": 30, "year": 365}
    if kwargs.get("last") is None:
        start = kwargs.get("start")
        end = kwargs.get("end")
    elif kwargs.get("last") is not None and (
        kwargs.get("start") is not None or kwargs.get("end") is not None
    ):
        print("Either enter 'from'/'to' dates or 'last', not both.")
        raise Exit(1)
    elif kwargs["last"] in literals.keys():
        days = literals[kwargs["last"]]
    else:
        try:
            days = kwargs["last"]
        except ValueError:
            print("'last' must be 'week', 'month', 'year', or a positive integer")
            raise Exit(1)
    if kwargs.get("last") is not None:
        end = datetime.now()
        start = end - timedelta(days=int(days))
    return start, end


from pandas._libs.tslibs.parsing import DateParseError
from memoryfm.cli.utils._common_utils import check_loaded
import json


def print_scrobbles(
    import_name: str | None = None,
    max_length: int | None = 10,
    meta: bool | None = False,
    from_date: str | None = None,
    to_date: str | None = None,
    last: str | int | None = None,
    by_artists: list[str] | None = None,
    by_albums: list[str] | None = None,
    by_tracks: list[str] | None = None,
    sort_by_date: bool = False,
    newest_first: bool | None = None,
) -> None:
    """Print ScrobbleLog"""
    start, end = date_filter(start=from_date, end=to_date, last=last)
    if import_name is None:
        import_name = check_loaded()
    try:
        scrobble_log = read_cache_from_name(
            import_name,
            start=start,
            end=end,
            artists=by_artists,
            albums=by_albums,
            tracks=by_tracks,
        )
    except FileNotFoundError:
        print("No import found for the username:", import_name)
        raise Exit(1)
    except DateParseError as e:
        print(e)
        raise Exit(2)
    if not sort_by_date and newest_first:
        print("If you want to sort, pass the --sort flag as well.")
        raise Exit(3)
    elif sort_by_date and newest_first is None:
        newest_first = False
    print(
        scrobble_log.to_markdown(
            maxcolwidths=4 * [20],
            tablefmt="pipe",
            max_length=max_length,
            show_extra=not meta,
            newest_first=newest_first,
        )
    )
    if meta:
        print(json.dumps(scrobble_log.meta, indent=4))


def cli_top_charts(
    import_name: str | None = None, kind: str = "tracks", n: int | None = 5, **kwargs
) -> None:
    """
    CLI top charts
    """
    start, end = date_filter(**kwargs)
    if import_name is None:
        import_name = check_loaded()
    if n is None:
        n = 5
    charts = read_cache_from_name(import_name, start=start, end=end).top_charts(kind, n)
    print(charts.to_markdown())
