"""create_analytics_view

Revision ID: bf0507c235e9
Revises: e1fef182da4c
Create Date: 2026-04-28 19:55:10.932525

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "bf0507c235e9"
down_revision: Union[str, Sequence[str], None] = "e1fef182da4c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
        CREATE OR REPLACE VIEW analytics_view AS
        SELECT
            s.id AS scrobble_id,
            s.timestamp,
            u.id AS user_id,
            u.username,
            t.id AS track_id,
            t.name AS track,
            al.id AS album_id,
            al.name AS album,
            ar.id AS artist_id,
            ar.name AS artist
        FROM scrobbles s
        JOIN users u ON s.user_id = u.id
        JOIN tracks t ON s.track_id = t.id
        JOIN albums al ON t.album_id = al.id
        JOIN artists ar ON t.artist_id = ar.id
    """)
    op.create_index(
        op.f("ix_scrobbles_user_id"), "scrobbles", ["user_id"], unique=False
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_scrobbles_user_id"), table_name="scrobbles")
    op.execute("DROP VIEW analytics_view")
