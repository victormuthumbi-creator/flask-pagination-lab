import os
import pytest
from app import create_app, db
from models import Book

@pytest.fixture(scope="module")
def test_client():
    os.environ["FLASK_ENV"] = "test"
    test_app = create_app("test")

    with test_app.test_client() as client:
        with test_app.app_context():
            db.create_all()
            seed_test_data()
        yield client
        with test_app.app_context():
            db.drop_all()


def seed_test_data():
    """Seed the in-memory test database with dummy books."""
    for i in range(1, 21):  # 20 books
        db.session.add(Book(title=f"Book {i}", author="Flatiron School"))
    db.session.commit()


def test_default_pagination(test_client):
    """Should return page 1 with default per_page (5)."""
    response = test_client.get("/books")
    data = response.get_json()

    assert response.status_code == 200
    assert data["page"] == 1
    assert data["per_page"] == 5
    assert len(data["items"]) == 5
    assert data["total"] == 20
    assert data["total_pages"] == 4


def test_specific_page_and_per_page(test_client):
    """Should return the correct page and number of records."""
    response = test_client.get("/books?page=2&per_page=3")
    data = response.get_json()

    assert response.status_code == 200
    assert data["page"] == 2
    assert data["per_page"] == 3
    assert len(data["items"]) == 3
    assert data["items"][0]["title"] == "Book 4"


def test_last_page_has_remaining_items(test_client):
    """The last page may return fewer than per_page if uneven total."""
    response = test_client.get("/books?page=4&per_page=6")
    data = response.get_json()

    assert response.status_code == 200
    assert data["page"] == 4
    assert len(data["items"]) == 2  # 6*3 = 18, 20-18 = 2 left


def test_empty_results_when_page_exceeds_total(test_client):
    """Should return an empty list but not crash if page exceeds total."""
    response = test_client.get("/books?page=99")
    data = response.get_json()

    assert response.status_code == 200
    assert data["items"] == []
    assert data["page"] == 99
    assert data["total"] == 20
    assert data["total_pages"] >= 1


def test_missing_params_fallback_to_defaults(test_client):
    """Requesting without query parameters should still work."""
    response = test_client.get("/books")
    data = response.get_json()

    assert response.status_code == 200
    assert data["page"] == 1
    assert data["per_page"] == 5
    assert len(data["items"]) == 5
