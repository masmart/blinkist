"""Load small, idempotent development fixtures after migrations."""
from datetime import datetime

from app import create_app
from config import db
from models.Category import Categories
from services.unit_of_work import transaction


DEFAULT_CATEGORIES = (
    {
        'name': 'توسعه فردی',
        'original_name': 'Personal Development',
        'slug': 'توسعه-فردی',
        'description': 'کتاب‌هایی برای ساخت عادت‌ها و رشد فردی.',
        'icon': 'book-open',
    },
)


def seed():
    with transaction() as session:
        for values in DEFAULT_CATEGORIES:
            if Categories.query.filter_by(slug=values['slug']).first():
                continue
            now = datetime.now()
            session.add(Categories(created_at=now, updated_at=now, **values))


if __name__ == '__main__':
    application = create_app()
    with application.app_context():
        seed()
        print('Development seed data loaded.')
