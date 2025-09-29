"""create book Table

Revision ID: b0807f85ea00
Revises: a3823713d6d2
Create Date: 2025-09-29 21:04:12.436126

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b0807f85ea00'
down_revision: Union[str, Sequence[str], None] = 'a3823713d6d2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'books',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('author', sa.String(), nullable=False),
        sa.Column('added_by_user_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ['added_by_user_id'],
            ['users.id'],
            ondelete='CASCADE'
        ),
    )


def downgrade() -> None:
    op.drop_table('books')
