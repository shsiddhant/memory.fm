from __future__ import annotations
from memoryfm.cli.utils._loader_utils import read_cache_from_name
from datetime import datetime, timedelta
from typer import Exit
from typing import List

def date_filter(
    **kwargs
) ->tuple[str, str]:
    literals = {"week": 7, "month": 30, "year": 365}
    if kwargs.get('last') is None:
        start = kwargs.get('start')
        end = kwargs.get('end')
    elif (
        kwargs.get('last') is not None and
        (kwargs.get('start') is not None or
         kwargs.get('end') is not None)
    ):
        print("Either enter 'from'/'to' dates or 'last', not both.")
        raise Exit(1)
    elif kwargs['last'] in literals.keys():
        days = literals.get(kwargs['last'])
    else:
        try:
            days = int(kwargs['last'])
        except ValueError:
            print("'last' must be 'week', 'month', 'year', or "
                  "a positive integer")
            raise Exit(1)
    if kwargs.get('last') is not None:
        end = datetime.now()
        start = end - timedelta(days=days)
    return start, end


def print_scrobbles(
    import_name: str = None,
    max_length: int = 10,
    meta: bool = False,
    from_date: str = None,
    to_date: str = None, 
    last: str | int | None = None,
    by_artists: List[str] = None,
    by_albums: List[str]= None,
    by_tracks: List[str] = None,
) -> None:
    """Print ScrobbleLog"""
    from memoryfm.cli.utils._loader_utils import read_cache_from_name
    from memoryfm.cli.utils._cli_printer import date_filter
    from pandas._libs.tslibs.parsing import DateParseError
    start, end = date_filter(start=from_date, end=to_date, last=last)
    try:
        scrobble_log = read_cache_from_name(
                    import_name, start=start, end=end, artists=by_artists,
                albums=by_albums, tracks=by_tracks
        )
    except DateParseError as e:
        print(e)
        raise Exit(2)
    print(scrobble_log.to_markdown(
            maxcolwidths=20, tablefmt="pipe", max_length=max_length,
            show_extra=not meta
    ))
    if meta:
        import json
        print(json.dumps(scrobble_log.meta, indent=4))


def cli_top_charts(
    import_name: str,
    kind: str = "tracks",
    n: int = 5,
    **kwargs
) ->None:
    """
    CLI top charts
    """
    start, end = date_filter(**kwargs)
    charts = read_cache_from_name(import_name, start=start,
                                end=end).top_charts(kind, n)
    print(charts.to_markdown())

