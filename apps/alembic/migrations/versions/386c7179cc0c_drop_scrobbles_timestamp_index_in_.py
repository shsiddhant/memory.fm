"""drop scrobbles timestamp index in favour of composite index

Revision ID: 386c7179cc0c
Revises: 6e78d39b140d
Create Date: 2026-05-18 06:17:41.594499

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "386c7179cc0c"
down_revision: Union[str, Sequence[str], None] = "6e78d39b140d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_index("ix_scrobbles_timestamp", table_name="scrobbles", if_exists=True)


def downgrade() -> None:
    """Downgrade schema."""
    op.create_index(
        "ix_scrobbles_timestamp",
        table_name="scrobbles",
        columns=["timestamp"],
        if_not_exists=True,
    )
