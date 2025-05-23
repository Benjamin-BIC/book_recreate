import json
from urllib import response
from fastapi.testclient import TestClient
from main import app
from schemas.book import BookCreate, BookUpdate

client = TestClient(app)


def test_get_books():
    response = client.get("/books")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_add_book():
    payload = {
        "title": "Johny bravo",
        "author": "John Doe",
        "year": 2023,
        "pages": 500,
        "language": "English"
    }
    response = client.post("/books", json=payload)
    data = response.json()
    assert data["message"] == "Book added successfully"
    assert data["data"]["title"] == "Johny bravo"


def test_get_book_by_id():
    payload = {
        "title": "Johny bravo",
        "author": "John Doe",
        "year": 2023,
        "pages": 500,
        "language": "English"
    }
    response = client.post("/books", json=payload)
    add_book_data = response.json()
    book_id = add_book_data['data']['id']
    get_response = client.get(f"/books/{book_id}")
    get_book_data = get_response.json()
    assert get_response.status_code == 200
    assert get_book_data['id'] == book_id


def test_get_book_by_id_not_found():
    book_id = 1
    get_response = client.get(f"/books/{book_id}")
    get_book_data = get_response.json()
    assert get_response.status_code == 404
    assert get_book_data['detail'] == "book not found."


def test_update_book():
    payload = {
        "title": "Johny bravo",
        "author": "John Doe",
        "year": 2023,
        "pages": 500,
        "language": "English"
    }
    response = client.put("/books", json=payload)
    assert response.status_code == 200
    original_book_data = response.json()['data']
    book_id = original_book_data['id']

    the_update = {
        "title": "Mikel Obi",
        "year": 2012
    }
    response = client.put(f"/books/{book_id}", json=the_update)
    updated_book_data = response.json()
    assert response.status_code == 200
    assert updated_book_data["id"] == book_id
    assert updated_book_data["title"] == "Mikel Obi"
    assert updated_book_data["author"] == "John Doe"
    assert updated_book_data["message"] == f"Book updated successfully"

    # verifying the update-book
    get_response = client.get(f"/books/{book_id}")
    assert get_response.status_code == 200
    verified_data = get_response.json()
    assert verified_data["id"] == book_id
    assert verified_data["year"] == 2012


def test_update_book_not_found():
    book_id = 5
    payload = {
        "title": "Tesla Optimus",
        "year": 2025
    }
    response = client.put(f"/books/{book_id}", json=payload)
    volatile_data = response.json()
    assert response.status_code == 404
    assert volatile_data["detail"] == "Book with id: {book_id} not found"


def test_delete_book():
    payload = {
        "title": "Johny bravo",
        "author": "John Doe",
        "year": 2023,
        "pages": 500,
        "language": "English"
    }
    response = client.post("/books", json=payload)
    book_data = response.json()["data"]
    book_id = book_data["id"]
    assert response.status_code == 200

    # delete request
    delete_response = client.delete(f"/books/{book_id}")
    assert delete_response.status_code == 200
    assert delete_response.json(
    )["message"] == f"Book deleted successfully"

    # verifying delete
    response_after_delete = client.get(f"/books/{book_id}")
    assert response_after_delete == 404
    assert response_after_delete.json(
    )["detail"] == f"Book with id: {book_id} not found"

    def test_delete_book_not_found():
        book_id = 11111  # non-existent id
        response = client.delete(f"/books/{book_id}")
        assert response.status_code == 404
        assert response.json()["detail"] == f"Book with id {book_id} not found"
