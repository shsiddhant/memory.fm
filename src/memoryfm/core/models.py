from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy import DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)

if TYPE_CHECKING:
    import datetime


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    tz: Mapped[str] = mapped_column(default="Etc/UTC")
    scrobbles: Mapped[list["Scrobble"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )


class Scrobble(Base):
    __tablename__ = "scrobble"

    id: Mapped[int] = mapped_column(primary_key=True)
    timestamp: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), index=True
    )
    track: Mapped[str]
    artist: Mapped[str]
    album: Mapped[str] = mapped_column(default="")
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="scrobbles")

    __table_args__ = UniqueConstraint(
        "timestamp", "track", "artist", "album", "user_id"
    )
