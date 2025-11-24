from __future__ import annotations

# from typing import TYPE_CHECKING
import streamlit as st

from memoryfm.streamlit.util import summary, set_session_data, scrobbles_count
from memoryfm.cli.utils._import_utils import get_imported_names


if "imports" not in st.session_state or st.session_state.imports is None:
    st.session_state["imports"] = get_imported_names()


# Reduce whitespace above header.
st.markdown(
    """
    <style>
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        padding-left: 5rem;
        padding-right: 5rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Header
if st.session_state.get("username") is not None:
    st.title(f":primary[{st.session_state.username}]")
    ""
    set_session_data(st.session_state.username)
    # Summary Badges
    card = summary(st.session_state["sc_log"])
    listens_key = card["listens_key"]
    timespan = st.container(border=True)
    with timespan:
        st.badge(
            f"**{card['listens_key'].rstrip('e')}ing since"
            f" {card['first'].df.timestamp[0].strftime('%B %d, %Y')}**",
            icon=":material/calendar_month:",
            color="violet",
        )
        badges = st.container()
    with badges:
        scrobblecount, average, tracks, artists, albums, *extra = st.columns(
            [4, 4, 3, 3, 3], gap="small", width=1000
        )
        with scrobblecount:
            st.badge(
                f"**{card[f'{listens_key}count']}** {listens_key}s",
                icon=":material/bar_chart:",
                color="primary",
                width="stretch",
            )
        with average:
            st.badge(
                f"**{int(card['average'])}** {listens_key}s a day",
                icon=":material/avg_pace:",
                color="yellow",
            )
        with tracks:
            tracks = st.badge(
                f"**{card['trackscount']}** Tracks",
                icon=":material/music_note:",
                color="orange",
                width="stretch",
            )
        with artists:
            st.badge(
                f"**{card['artistscount']}** Artists",
                icon=":material/artist:",
                color="blue",
            )
        with albums:
            st.badge(
                f"**{card['albumscount']}** Albums",
                icon=":material/album:",
                color="green",
            )
    ""
    ""
    # Scrobbles count plot
    sclog = st.session_state["sc_log"]
    count = scrobbles_count(sclog)
    st.bar_chart(
        count,
        x="Year",
        y="Scrobbles",
        x_label="Scrobbles",
        y_label="Year",
        horizontal=True,
        color="#B40B08",
        height=300,
    )

    # Top Charts preview
    top_tracks, top_artists, top_albums = st.columns(3, border=True)
    with top_tracks:
        "**:orange[:material/music_note: Top Tracks]**"
        st.markdown(sclog.top_charts().head(3).to_markdown())
    with top_artists:
        "**:blue[:material/artist: Top Artists]**"
        st.write(sclog.top_charts("artist").head(3).to_markdown())
    with top_albums:
        "**:green[:material/album: Top Albums]**"
        st.write(sclog.top_charts("album").head(3).to_markdown())
