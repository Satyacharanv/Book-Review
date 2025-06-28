import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

book_response_mock = {
    "id": 1,
    "title": "The Pragmatic Programmer",
    "author": "Andy Hunt",
    "reviews": []
}

review_response_mock = {
    "id": 1,
    "review_text": "Excellent book!",
    "rating": 5,
    "book_id": 1
}

@pytest.mark.asyncio
@patch("app.routes.books.get_books_service", new_callable=AsyncMock)
def test_get_books(mock_get_books):
    mock_get_books.return_value = [book_response_mock]
    response = client.get("/books/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json()[0]["title"] == "The Pragmatic Programmer"

@pytest.mark.asyncio
@patch("app.routes.books.create_book_service", new_callable=AsyncMock)
def test_create_book(mock_create_book):
    mock_create_book.return_value = book_response_mock
    payload = {"title": "The Pragmatic Programmer", "author": "Andy Hunt"}
    response = client.post("/books/", json=payload)
    assert response.status_code == 201
    assert response.json()["id"] == 1
    assert response.json()["title"] == "The Pragmatic Programmer"

@pytest.mark.asyncio
@patch("app.routes.books.get_book_reviews_service", new_callable=AsyncMock)
def test_get_book_reviews(mock_get_reviews):
    mock_get_reviews.return_value = [review_response_mock]
    response = client.get("/books/1/reviews")
    assert response.status_code == 200
    assert response.json()[0]["review_text"] == "Excellent book!"

@pytest.mark.asyncio
@patch("app.routes.books.create_review_service", new_callable=AsyncMock)
def test_create_review(mock_create_review):
    mock_create_review.return_value = review_response_mock
    payload = {"review_text": "Excellent book!", "rating": 5}
    response = client.post("/books/1/reviews", json=payload)
    assert response.status_code == 201
    assert response.json()["rating"] == 5
