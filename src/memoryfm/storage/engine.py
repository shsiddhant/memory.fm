from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy import create_engine

from memoryfm.config import DB_URL

if TYPE_CHECKING:
    from sqlalchemy import Engine

engine: Engine = create_engine(DB_URL, pool_size=5, max_overflow=10, pool_pre_ping=True)
