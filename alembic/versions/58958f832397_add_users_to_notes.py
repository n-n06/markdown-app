"""Add users to notes

Revision ID: 58958f832397
Revises: 500309287e93
Create Date: 2025-06-30 01:07:18.368399

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '58958f832397'
down_revision: Union[str, Sequence[str], None] = '500309287e93'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('notes', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'notes', 'user', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'notes', type_='foreignkey')
    op.drop_column('notes', 'user_id')
    # ### end Alembic commands ###
