"""Add integrity constraints and lookup indexes.

Revision ID: a41f0c9d2e10
Revises: 8c63bb15cb3f
"""
from alembic import op
import sqlalchemy as sa


revision = 'a41f0c9d2e10'
down_revision = '8c63bb15cb3f'
branch_labels = None
depends_on = None


def upgrade():
    op.create_index('ix_books_slug', 'books', ['slug'], unique=True)
    op.create_index('ix_categories_slug', 'categories', ['slug'], unique=True)
    op.create_index('ix_collections_slug', 'collections', ['slug'], unique=True)
    op.create_index('ix_objects_object_name', 'objects', ['object_name'], unique=True)
    op.create_index('ix_ideas_book_id', 'ideas', ['book_id'])
    op.create_index('ix_audios_book_id', 'audios', ['book_id'])
    op.create_index('ix_topics_category_id', 'topics', ['category_id'])
    op.create_index('ix_bookmarks_user_id', 'bookmarks', ['user_id'])
    op.create_index('ix_bookmarks_book_id', 'bookmarks', ['book_id'])
    op.create_index(
        'uq_active_bookmark_user_book',
        'bookmarks',
        ['user_id', 'book_id'],
        unique=True,
        postgresql_where=sa.text('deleted_at IS NULL'),
    )


def downgrade():
    op.drop_index('uq_active_bookmark_user_book', table_name='bookmarks')
    op.drop_index('ix_bookmarks_book_id', table_name='bookmarks')
    op.drop_index('ix_bookmarks_user_id', table_name='bookmarks')
    op.drop_index('ix_topics_category_id', table_name='topics')
    op.drop_index('ix_audios_book_id', table_name='audios')
    op.drop_index('ix_ideas_book_id', table_name='ideas')
    op.drop_index('ix_objects_object_name', table_name='objects')
    op.drop_index('ix_collections_slug', table_name='collections')
    op.drop_index('ix_categories_slug', table_name='categories')
    op.drop_index('ix_books_slug', table_name='books')
