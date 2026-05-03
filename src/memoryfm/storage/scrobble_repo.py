from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy import delete, func, select, tuple_
from sqlalchemy.dialects.postgresql import insert

from memoryfm.models.core import Album, Artist, Scrobble, Track

if TYPE_CHECKING:
    from collections.abc import Sequence
    from sqlalchemy.orm import Session
    from datetime import datetime


def get_scrobbles_by_user(
    session: Session, user_id: int, limit: int | None = None, offset: int | None = None
) -> Sequence[Scrobble]:
    stmt = (
        select(Scrobble).where(Scrobble.user_id == user_id).limit(limit).offset(offset)
    )
    return session.scalars(stmt).fetchall()


def insert_scrobbles_by_user(session: Session, user_id: int, scrobbles: Sequence[dict]):
    unique_artists = {s["artist"] for s in scrobbles}
    unique_albums = {(s["album"], s["artist"]) for s in scrobbles}
    unique_tracks = {(s["track"], s["album"], s["artist"]) for s in scrobbles}

    # Insert artists
    stmt_artists = insert(Artist).on_conflict_do_nothing(
        index_elements=["name"],
    )
    session.execute(stmt_artists, [{"name": name} for name in unique_artists])

    artists_data = session.execute(
        select(Artist.name, Artist.id).filter(Artist.name.in_(unique_artists))
    )

    artists_map = {row.name: row.id for row in artists_data}
    # Insert albums
    stmt_albums = insert(Album).on_conflict_do_nothing(
        index_elements=["name", "artist_id"]
    )
    albums_insert = [
        {"name": name, "artist_id": artists_map[artist]}
        for (name, artist) in unique_albums
    ]
    session.execute(stmt_albums, albums_insert)
    albums_data = session.execute(
        select(Album.id, Album.artist_id, Album.name).filter(
            tuple_(Album.name, Album.artist_id).in_(
                [(album, artists_map[artist]) for (album, artist) in unique_albums]
            )
        )
    )
    albums_map = {(row.name, row.artist_id): row.id for row in albums_data}

    # Insert Track
    stmt_tracks = insert(Track).on_conflict_do_nothing(
        index_elements=["name", "album_id"],
    )
    tracks_insert = [
        {
            "name": name,
            "album_id": albums_map[(album, artists_map[artist])],
            "artist_id": artists_map[artist],
        }
        for (name, album, artist) in unique_tracks
    ]
    session.execute(stmt_tracks, tracks_insert)

    tracks_data = session.execute(
        select(Track.id, Track.name, Track.album_id, Track.artist_id).filter(
            tuple_(Track.name, Track.album_id, Track.artist_id).in_(
                [
                    (
                        track,
                        albums_map[(album, artists_map[artist])],
                        artists_map[artist],
                    )
                    for (track, album, artist) in unique_tracks
                ]
            )
        )
    )
    tracks_map = {
        (row.name, row.album_id, row.artist_id): row.id for row in tracks_data
    }

    # Insert Scrobbles
    stmt = insert(Scrobble).on_conflict_do_nothing(
        index_elements=["timestamp", "track_id", "user_id"],
    )
    scrobbles_insert = [
        {
            "user_id": user_id,
            "track_id": tracks_map[
                (
                    s["track"],
                    albums_map[(s["album"], artists_map[s["artist"]])],
                    artists_map[(s["artist"])],
                )
            ],
            **s,
        }
        for s in scrobbles
    ]
    session.execute(stmt, scrobbles_insert)


def get_end_timestamps_by_user(
    session: Session, user_id: int
) -> tuple[datetime, datetime] | None:
    stmt = select(func.min(Scrobble.timestamp), func.max(Scrobble.timestamp)).where(
        Scrobble.user_id == user_id
    )
    data = session.execute(stmt).fetchone()
    if data:
        return data.tuple()
    return None


def delete_scrobbles_by_user(
    session: Session,
    user_id: int,
    from_ts: datetime | None = None,
    to_ts: datetime | None = None,
):
    stmt = delete(Scrobble).where(Scrobble.user_id == user_id)

    if from_ts:
        stmt = stmt.where(Scrobble.timestamp >= from_ts)
    if to_ts:
        stmt = stmt.where(Scrobble.timestamp <= to_ts)

    session.execute(stmt)
