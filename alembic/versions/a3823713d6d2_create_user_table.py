"""create user Table

Revision ID: a3823713d6d2
Revises: 
Create Date: 2025-09-29 20:54:38.033458

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a3823713d6d2'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )

    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('users')
    pass


# def upgrade() -> None:
#     op.create_table(
#         'books',
#         sa.Column('id', sa.Integer(), primary_key=True, index=True),
#         sa.Column('title', sa.String(), nullable=False),
#         sa.Column('author', sa.String(), nullable=False),
#         sa.Column('added_by_user_id', sa.Integer(), nullable=False),
#         sa.ForeignKeyConstraint(
#             ['added_by_user_id'],
#             ['users.id'],
#             ondelete='CASCADE'
#         ),
#     )


# def downgrade() -> None:
#     op.drop_table('books')
