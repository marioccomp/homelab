"""create folder table

Revision ID: b9f7065342a1
Revises: 94abbe7fb214
Create Date: 2026-10-25 17:09:32.067769

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b9f7065342a1'
down_revision: Union[str, Sequence[str], None] = '94abbe7fb214'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('folders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('size_bytes', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_folders_id'), 'folders', ['id'], unique=False)
    op.add_column('files', sa.Column('folder_id', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_file_folder', 'files', 'folders', ['folder_id'], ['id'])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('fk_file_folder', 'files', type_='foreignkey')
    op.drop_column('files', 'folder_id')
    op.drop_index(op.f('ix_folders_id'), table_name='folders')
    op.drop_table('folders')
