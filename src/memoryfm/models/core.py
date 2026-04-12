from __future__ import annotations
from sqlalchemy import DateTime, ForeignKey, UniqueConstraint, String
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)


import datetime  # noqa: TC003


class Base(DeclarativeBase):
    pass


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
    scrobbles: Mapped[list["Scrobble"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
        doc="List of scrobbles of the user.",
    )


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
    """Album"""
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), doc="User id of the scrobble."
    )
    user: Mapped["User"] = relationship(
        back_populates="scrobbles", doc="User of the scrobble in the user table."
    )

    __table_args__ = (
        UniqueConstraint("timestamp", "track", "artist", "album", "user_id"),
    )
