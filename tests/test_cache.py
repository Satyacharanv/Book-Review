import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

cached_books_mock = [
    {
        "id": 1,
        "title": "Redis in Action",
        "author": "Josiah Carlson",
        "reviews": []
    }
]

@pytest.mark.asyncio
@patch("app.services.book_service.redis_cache.get_json", new_callable=AsyncMock)
@patch("app.services.book_service.redis_cache.set_json", new_callable=AsyncMock)
def test_redis_cache_hit(mock_set, mock_get):
    mock_get.return_value = cached_books_mock
    response = client.get("/books/")
    assert response.status_code == 200
    assert response.json()[0]["title"] == "Redis in Action"
    mock_set.assert_not_called()

@pytest.mark.asyncio
@patch("app.services.book_service.redis_cache.set_json", new_callable=AsyncMock)
@patch("app.services.book_service.redis_cache.get_json", new_callable=AsyncMock)
@patch("app.routes.books.get_books_service", new_callable=AsyncMock)
def test_redis_cache_miss_then_set(mock_get_books_service, mock_get_json, mock_set_json):
    mock_get_json.return_value = None
    mock_set_json.return_value = True
    mock_get_books_service.return_value = cached_books_mock

    response = client.get("/books/")
    assert response.status_code == 200
    assert response.json()[0]["title"] == "Redis in Action"
