import pytest

from app import app


@pytest.fixture()
def client():
    app.config.update(TESTING=True, WTF_CSRF_ENABLED=False)
    with app.test_client() as test_client:
        yield test_client


def test_admin_requires_authentication(client):
    response = client.get('/admin/')
    assert response.status_code == 401


def test_upload_requires_authentication(client):
    response = client.get('/upload/')
    assert response.status_code == 401


def test_bookmark_requires_authentication(client):
    response = client.post('/book/bookmark', data={'book_id': '1'})
    assert response.status_code == 401
