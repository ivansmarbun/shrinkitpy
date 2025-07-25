import pytest
from app import app


@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client


def test_index_get(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"<form" in response.data


def test_index_post(client):
    response = client.post("/", data={"url": "https://example.com"})
    assert response.status_code == 200
    assert b"Shortened URL:" in response.data


def test_shorten_post(client):
    response = client.post("/shorten", json={"url": "https://example.com"})
    assert response.status_code == 200
    assert b"short_url" in response.data


def test_shorten_post_missing_url(client):
    response = client.post("/shorten", json={})
    assert response.status_code == 400
    assert b"Missing URL" in response.data


def test_redirect_short_url_not_found(client):
    response = client.get("/s/invalidid")
    assert response.status_code == 404
    assert b"URL not found" in response.data


def test_analytics_get(client):
    response = client.get("/analytics")
    assert response.status_code == 200
    assert b"<form" in response.data


def test_analytics_post_missing_short_url(client):
    response = client.post("/analytics", json={})
    assert response.status_code == 400
    assert b"Missing short_url" in response.data
