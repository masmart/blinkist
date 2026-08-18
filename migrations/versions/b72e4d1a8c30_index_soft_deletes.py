"""Index soft-delete columns.

Revision ID: b72e4d1a8c30
Revises: a41f0c9d2e10
"""
from alembic import op


revision = 'b72e4d1a8c30'
down_revision = 'a41f0c9d2e10'
branch_labels = None
depends_on = None

TABLES = ('authors', 'audios', 'bookmarks', 'books', 'categories', 'collections', 'curators', 'ideas', 'objects', 'users')


def upgrade():
    for table in TABLES:
        op.create_index(f'ix_{table}_deleted_at', table, ['deleted_at'])


def downgrade():
    for table in reversed(TABLES):
        op.drop_index(f'ix_{table}_deleted_at', table_name=table)
