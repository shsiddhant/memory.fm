"""drop artists, albums, tracks columns from scrobbles table

Revision ID: 6e78d39b140d
Revises: bf0507c235e9
Create Date: 2026-05-08 13:46:33.383371

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "6e78d39b140d"
down_revision: Union[str, Sequence[str], None] = "bf0507c235e9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_column("scrobbles", "track")
    op.drop_column("scrobbles", "album")
    op.drop_column("scrobbles", "artist")


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column("scrobbles", sa.Column("album", sa.VARCHAR(), nullable=True))
    op.add_column("scrobbles", sa.Column("track", sa.VARCHAR(), nullable=True))
    op.add_column("scrobbles", sa.Column("artist", sa.VARCHAR(), nullable=True))
