"""empty message

Revision ID: 7d6d4747b222
Revises: 14896f976bdd
Create Date: 2024-12-30 18:40:45.108049

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7d6d4747b222'
down_revision: Union[str, None] = '14896f976bdd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
