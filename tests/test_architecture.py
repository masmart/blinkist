from datetime import datetime

import pytest

from app import create_app
from models.Book import Book, Books
from models.Category import Categories, Category
from models.User import Bookmark, Bookmarks, User, Users
from services.storage import StorageService
from services import unit_of_work


def test_application_factory_creates_isolated_apps():
    overrides = {'SQLALCHEMY_DATABASE_URI': 'sqlite://'}
    first = create_app('testing', overrides)
    second = create_app('testing', overrides)

    assert first is not second
    assert first.testing and second.testing
    assert first.name == 'app'


def test_production_requires_secret_key(monkeypatch):
    import config

    monkeypatch.setattr(config.ProductionConfig, 'SECRET_KEY', None)
    with pytest.raises(RuntimeError, match='SECRET_KEY'):
        config.get_config('production')


def test_singular_model_aliases_remain_backwards_compatible():
    assert Book is Books
    assert Category is Categories
    assert User is Users
    assert Bookmark is Bookmarks


def test_slug_constraints_are_declared_on_models():
    assert Books.__table__.c.slug.unique is True
    assert Books.__table__.c.slug.index is True
    assert Categories.__table__.c.slug.unique is True


def test_soft_delete_marks_entity_and_active_query_exists():
    book = Books()
    assert book.deleted_at is None

    book.soft_delete()

    assert isinstance(book.deleted_at, datetime)
    assert callable(Books.active)


class FakeStorageClient:
    def __init__(self, exists=False):
        self.exists = exists
        self.created = []

    def bucket_exists(self, bucket):
        return self.exists

    def make_bucket(self, bucket):
        self.created.append(bucket)


def test_storage_service_accepts_injected_client():
    client = FakeStorageClient()
    service = StorageService(client=client)

    service.ensure_bucket('audio')

    assert client.created == ['audio']


class FakeSession:
    def __init__(self):
        self.commits = 0
        self.rollbacks = 0

    def commit(self):
        self.commits += 1

    def rollback(self):
        self.rollbacks += 1


def test_transaction_commits_once(monkeypatch):
    session = FakeSession()
    monkeypatch.setattr(unit_of_work.db, 'session', session)

    with unit_of_work.transaction() as active_session:
        assert active_session is session

    assert session.commits == 1
    assert session.rollbacks == 0


def test_transaction_rolls_back_on_failure(monkeypatch):
    session = FakeSession()
    monkeypatch.setattr(unit_of_work.db, 'session', session)

    with pytest.raises(ValueError):
        with unit_of_work.transaction():
            raise ValueError('boom')

    assert session.commits == 0
    assert session.rollbacks == 1
