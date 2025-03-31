import sys
import os
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from main import app
from database import collection

client = TestClient(app)

# Clear DB before and after each test 
@pytest.fixture(autouse=True, scope="function")
def clear_test_collection():
    collection.delete_many({})
    yield
    collection.delete_many({})

# ------------------ GET ------------------ #

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200

def test_get_courses():
    response = client.get("/courses/")
    assert response.status_code == 200
    assert "courses" in response.json()

def test_get_notes():
    response = client.get("/notes/")
    assert response.status_code == 200
    assert "notes" in response.json()

def test_get_summaries():
    response = client.get("/summaries/")
    assert response.status_code == 200
    assert "summaries" in response.json()

def test_get_practicetests():
    response = client.get("/practicetests/")
    assert response.status_code == 200
    assert "practicetests" in response.json()

# ------------------ POST ------------------ #

def test_post_course():
    response = client.post("/courses", json={
        "type": "course",
        "course": "TST101",
        "title": "Test Course"
    })
    assert response.status_code == 201
    assert "course" in response.json()

def test_post_note():
    response = client.post("/notes", json={
        "type": "note",
        "course": "TST101",
        "title": "Test Note",
        "chapter": 1,
        "text": "This is a valid test note with more than ten characters."
    })
    assert response.status_code == 201
    assert "note" in response.json()

def test_post_note_invalid_text():
    response = client.post("/notes", json={
        "type": "note",
        "course": "TST101",
        "title": "Bad Note",
        "chapter": 1,
        "text": "short"
    })
    assert response.status_code == 422

@patch("openaiAPI.generate_test_from_notes")
def test_post_practicetest(mock_generate):
    mock_generate.return_value = [
        {"question": "What is Python?", "answer": "A programming language."}
    ]
    client.post("/notes", json={
        "type": "note",
        "course": "TST101",
        "title": "Test Note",
        "chapter": 1,
        "text": "This is a valid note for practice test generation."
    })
    response = client.post("/practicetests?num_questions=1", json={"type": "note", "course": "TST101"})
    assert response.status_code == 201
    assert "inserted" in response.json()

@patch("openaiAPI.generate_summary_from_notes")
def test_post_summary(mock_generate):
    mock_generate.return_value = {
        "summary": {"description": "Summary of content."}
    }
    client.post("/notes", json={
        "type": "note",
        "course": "TST101",
        "title": "Test Note",
        "chapter": 1,
        "text": "This is valid content for generating a summary."
    })
    response = client.post("/summaries", json={"type": "note", "course": "TST101"})
    assert response.status_code == 201
    assert "inserted" in response.json()

# ------------------ PATCH ------------------ #

def test_patch_note():
    note = {
        "type": "note",
        "course": "TST101",
        "title": "Old Title",
        "chapter": 1,
        "text": "This is a test note."
    }
    insert = client.post("/notes", json=note).json()["note"]
    response = client.patch(f"/notes/{insert['_id']}", json={"title": "New Title"})
    assert response.status_code == 200
    assert response.json()["updated_document"]["title"] == "New Title"

# ------------------ DELETE ------------------ #

def test_delete_note():
    note = {
        "type": "note",
        "course": "TST101",
        "title": "To Delete",
        "chapter": 1,
        "text": "This is a note to be deleted."
    }
    inserted = client.post("/notes", json=note).json()["note"]
    response = client.delete(f"/{inserted['_id']}")
    assert response.status_code == 200
    assert response.json()["message"] == "Document deleted"
