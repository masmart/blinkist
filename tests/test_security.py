import pytest

from app import create_app


@pytest.fixture()
def client():
    app = create_app('testing', {'SQLALCHEMY_DATABASE_URI': 'sqlite://'})
    with app.test_client() as test_client:
        yield test_client


def test_admin_requires_authentication(client):
    response = client.get('/admin/')
    assert response.status_code == 401


def test_upload_requires_authentication(client):
    response = client.get('/upload/')
    assert response.status_code == 302
    assert response.headers['Location'].startswith('/user/login')


def test_bookmark_requires_authentication(client):
    response = client.post('/book/bookmark', data={'book_id': '1'})
    assert response.status_code == 302
    assert response.headers['Location'].startswith('/user/login')
