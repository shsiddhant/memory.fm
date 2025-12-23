from __future__ import annotations
from typing import TYPE_CHECKING
import streamlit as st
import json
from datetime import datetime

from memoryfm.cli.utils._loader_utils import read_cache_from_name
from memoryfm.cli.utils._import_utils import read_imports
from memoryfm.cli.utils._cli_printer import date_filter
from memoryfm.cli.utils._common_utils import check_loaded
from memoryfm.cli import imports_dir, imports_file, loaded_file


if TYPE_CHECKING:
    from memoryfm import ScrobbleLog
    import pandas as pd
    from typing import Literal


def _delete_import(username: str):
    imports_list = read_imports()
    name_imported_data = next(
        (d for d in imports_list if d.get("importname") == username), None
    )
    imports_list.remove(name_imported_data)
    with open(imports_file, "w") as fp:
        json.dump(imports_list, fp, indent=4)
    meta_file = imports_dir / f"{username}" / f"{username}-meta.json"
    df_file = imports_dir / f"{username}" / f"{username}-df.parquet"
    meta_file.unlink()
    df_file.unlink()
    (imports_dir / f"{username}").rmdir()
    if loaded_file.is_file() and check_loaded() == username:
        loaded_file.unlink()


from memoryfm.cli.utils._loader_utils import _load_saved_log


def set_session_data(
    username: str,
    max_length: int = 10,
    from_date: str | None = None,
    to_date: str | None = None,
    **kwargs,
) -> None:
    if username is not None:
        st.session_state["username"] = username
        st.session_state["max"] = max_length
        st.session_state["sc_log"] = read_cache_from_name(
            username, start=from_date, end=to_date, **kwargs
        )
        _load_saved_log(username)
        if from_date is None:
            st.session_state["from"] = datetime.fromisoformat(
                st.session_state["sc_log"].meta["date_range"]["start"]
            )
        else:
            st.session_state["from"] = from_date
        if to_date is None:
            st.session_state["to"] = datetime.fromisoformat(
                st.session_state["sc_log"].meta["date_range"]["end"]
            )
        else:
            st.session_state["to"] = to_date
        if from_date is None and to_date is None:
            st.session_state["date_range"] = "All Time"
        else:
            st.session_state["date_range"] = (
                f"{st.session_state['from'].strftime('%d %b %Y')} to"
                f" {st.session_state['to'].strftime('%d %b %Y')}"
            )
        st.session_state["meta"] = st.session_state["sc_log"].meta
    else:
        raise RuntimeError


def summary(scrobble_log) -> str:
    meta = scrobble_log.meta
    if meta["source"] == "spotify":
        listens = "num_listens"
        listens_key = "Listen"
    else:
        listens = "num_scrobbles"
        listens_key = "Scrobble"

    card = {
        f"{listens_key}count": len(scrobble_log),
    }
    for kind in ("track", "artist", "album"):
        card[f"{kind}scount"] = scrobble_log.df[kind].nunique()
    first = scrobble_log[0:1]  # .to_markdown(show_extra=False)
    last = scrobble_log[-1:]  # .to_markdown(show_extra=False)
    card["first"] = first
    card["last"] = last
    card["listens"] = listens
    card["listens_key"] = listens_key
    timerng = (last.df.loc[0, "timestamp"] - first.df.loc[0, "timestamp"]).days
    if not timerng:
        timerng = 1
    card["average"] = len(scrobble_log) / timerng

    #    summary = f"""
    # **Username:** {meta["username"]}
    #
    # **Timezone:** {meta["tz"]}
    #
    # **Platform:** {meta["source"].capitalize()}
    #
    # **{listens_key}s:** {meta[listens]}
    #
    # **First {listens_key}:**
    #
    # {first}
    #
    # **Last {listens_key}:**
    #
    # {last}
    #    """
    return card


def date_popover():
    with st.popover(
        st.session_state.get("date_range"),
        icon=":material/calendar_today:",
    ):
        st.write("Select a date range")
        from_date = st.date_input(
            label="From",
            value=st.session_state.get("from"),
            format="DD-MM-YYYY",
        )
        to_date = st.date_input(
            label="To",
            value=st.session_state.get("to"),
            format="DD-MM-YYYY",
        )
        return from_date, to_date


def print_scrobbles(
    username: str,
    max_length: int = 10,
    from_date: str | None = None,
    to_date: str | None = None,
) -> None:
    try:
        set_session_data(username, max_length, from_date, to_date)
    except RuntimeError:
        st.error("Please select a username first.")
        st.stop()
    else:
        st.dataframe(
            st.session_state["sc_log"].head(max_length).df,
            row_height=70,
            hide_index=True,
        )


def scrobbles_count(
    sc_log: ScrobbleLog,
) -> pd.DataFrame:
    ts = sc_log.df.timestamp.copy()
    ts.index = ts.dt.year
    count = ts.groupby(level=0).count()
    count.name = "Scrobbles"
    count.index.name = "Year"
    count = count.reset_index()
    return count


# Time Periods
# ---------------------------------------------------------------------------
def time_periods(
    value: Literal["week", "month", "year", "all time", "custom date range"] = "week",
):
    index_dict = {
        "week": 0,
        "month": 1,
        "year": 2,
        "all time": 3,
        "custom date range": 4,
    }
    st.markdown("#### :material/calendar_today: Time Period")
    time_period = st.radio(
        "Time period",
        options=index_dict.keys(),
        index=index_dict[value],
        horizontal=True,
        label_visibility="collapsed",
        format_func=str.title,
    )
    if time_period in ["week", "month", "year"]:
        from_date, to_date = date_filter(last=time_period)
        from_date = from_date.date()
        to_date = to_date.date()
    elif time_period == "all time":
        from_date, to_date = None, None
    elif time_period == "custom date range":
        from_date_col, to_date_col = st.columns([1, 1])
        with from_date_col:
            from_date = st.date_input(
                label="**From**",
                value=st.session_state.get("from"),
                format="DD-MM-YYYY",
            )
        with to_date_col:
            to_date = st.date_input(
                label="**To**",
                value=st.session_state.get("to"),
                format="DD-MM-YYYY",
            )
    return from_date, to_date


icons = {"artists": "artist", "albums": "album", "tracks": "music_note"}
colors = {"artists": "blue", "albums": "green", "tracks": "orange"}
filters_allowed = {
    "artists": None,
    "albums": ["artists"],
    "tracks": ["artists", "albums"],
}


def format_chart_type(text: Literal["artists", "albums", "tracks"]):
    return f":material/{icons[text]}: {text.capitalize()}"


def analytics_base_layout(page_name: str, **kwargs):
    # Date Range
    if "date_range" not in st.session_state:
        st.session_state["date_range"] = "All Time"
    with st.container():
        kind_col, dates_col = st.columns([3, 3], border=True)
    with dates_col:
        from_date, to_date = time_periods(**kwargs)
    # Update Session State
    dates = {"from_date": from_date, "to_date": to_date}
    # Select Chart Type
    with kind_col:
        st.markdown("#### :material/view_list: Type")
        kind = st.radio(
            label="Type",
            options=["artists", "albums", "tracks"],
            label_visibility="collapsed",
            key=page_name,
            horizontal=True,
            format_func=format_chart_type,
        )
    return {"dates": dates, "kind": kind}
