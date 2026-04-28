from __future__ import annotations
from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    UniqueConstraint,
    String,
    func,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    validates,
)


import datetime  # noqa: TC003


class Base(DeclarativeBase):
    pass


class Artist(Base):
    """
    Represents a single artist in the database.
    """

    __tablename__ = "artists"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(), unique=True, doc="Artist name.")


class Album(Base):
    """
    Represents an album in the database.
    """

    __tablename__ = "albums"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(), doc="Album name.")
    artist_id: Mapped[int] = mapped_column(ForeignKey("artists.id"), index=True)

    __table_args__ = (UniqueConstraint("name", "artist_id"),)


class Track(Base):
    """
    Represents a track in the database
    """

    __tablename__ = "tracks"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(), doc="Track name.")

    album_id: Mapped[int] = mapped_column(ForeignKey("albums.id"), index=True)
    artist_id: Mapped[int] = mapped_column(ForeignKey("artists.id"), index=True)

    __table_args__ = (UniqueConstraint("name", "album_id"),)


class User(Base):
    """
    Represents a user in the database.
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True, doc="Unique integer id of the user."
    )
    username: Mapped[str] = mapped_column(
        unique=True,
        nullable=False,
        doc="Username of the user. Must be unique and not null.",
    )
    tz: Mapped[str] = mapped_column(
        server_default="Etc/UTC",
        doc="Timezone of the user. All time of the day analytics are based on it.",
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        doc="Timestamp at which user was created.",
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        doc="Timestamp at which user was last updated.",
    )
    scrobbles: Mapped[list["Scrobble"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
        doc="List of scrobbles of the user.",
    )

    __table_args__ = (
        CheckConstraint(
            func.length(func.trim(username)) > 0, name="username_not_blank"
        ),
    )

    @validates("username")
    def validate_username(self, key, value: str):
        if value is not None and not value.strip():
            raise ValueError("Username cannot be empty or only whitespace")
        return value


class Scrobble(Base):
    """
    Represents a single scrobble entry in the database.
    """

    __tablename__ = "scrobbles"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        doc="Unique id for the scrobble. "
        "It serves as the primary key of scrobble table.",
    )
    timestamp: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        index=True,
        doc="Timestamp at which the track was scrobbled. "
        "Stored as UTC with timezone awareness.",
    )
    track: Mapped[str] = mapped_column(
        String(), doc="Name/title of the scrobbled track."
    )
    artist: Mapped[str] = mapped_column(
        String(), doc="Artist name for the scrobbled track."
    )
    album: Mapped[str] = mapped_column(
        String(),
        server_default="",
        doc="(Optional) Album name for the scrobbled track.",
    )

    track_id: Mapped[int] = mapped_column(ForeignKey("tracks.id"), index=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), doc="User id of the scrobble."
    )
    user: Mapped["User"] = relationship(
        back_populates="scrobbles", doc="User of the scrobble in the user table."
    )

    __table_args__ = (UniqueConstraint("timestamp", "track_id", "user_id"),)
