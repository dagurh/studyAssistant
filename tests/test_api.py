import sys
import os
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from dotenv import load_dotenv

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

load_dotenv(".env.test", override=True)

from main import app

from database import collection

client = TestClient(app)

# ------------------ SETUP ------------------ #
def clear_test_collection():
    collection.delete_many({})

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkYWg1OEBoaS5pcyIsImV4cCI6MTc0NDYzOTY4Mn0.Lw4OPlGqWH1CLyQCh1p-PF2E7UhWuNKKZczaZgk5TdU"

patchDeleteID = None

clear_test_collection()

headers = {"Authorization": f"Bearer {token}"}

# ------------------ POST ------------------ #

def test_post_course():
    response = client.post("/courses", headers=headers, json={
        "type": "course",
        "course": "TST101",
        "title": "Test Course"
    })
    assert response.status_code == 201
    assert "course" in response.json()

def test_post_note():
    response = client.post("/notes", headers=headers, json={
        "type": "note",
        "course": "TST101",
        "title": "Test Note",
        "chapter": 1,
        "text": "This is a valid test note with more than ten characters."
    })
    assert response.status_code == 201
    assert "note" in response.json()

def test_post_note_invalid_text():
    response = client.post("/notes", headers=headers, json={
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
    client.post("/notes", headers=headers, json={
        "type": "note",
        "course": "TST101",
        "title": "Test Note",
        "chapter": 1,
        "text": "This is a valid note for practice test generation."
    })
    response = client.post("/practicetests?num_questions=1", headers=headers, json={"type": "note", "course": "TST101"})
    assert response.status_code == 201
    assert "inserted" in response.json()

@patch("openaiAPI.generate_summary_from_notes")
def test_post_summary(mock_generate):
    mock_generate.return_value = {
        "summary": {"description": "Summary of content."}
    }
    client.post("/notes", headers=headers, json={
        "type": "note",
        "course": "TST101",
        "title": "Test Note",
        "chapter": 1,
        "text": "This is valid content for generating a summary."
    })
    response = client.post("/summaries", headers=headers, json={"type": "note", "course": "TST101"})
    assert response.status_code == 201
    assert "inserted" in response.json()

# ------------------ GET ------------------ #

def test_read_root():
    response = client.get("/", headers=headers)
    assert response.status_code == 200

def test_get_courses():
    response = client.get("/courses/", headers=headers)
    assert response.status_code == 200

def test_get_notes():
    response = client.get("/notes/", headers=headers)
    firstID = response.json()["notes"][0]["_id"]
    global patchDeleteID
    patchDeleteID = firstID
    assert response.status_code == 200
def test_get_summaries():
    response = client.get("/summaries/", headers=headers)
    assert response.status_code == 200

def test_get_practicetests():
    response = client.get("/practicetests/", headers=headers)
    assert response.status_code == 200

# ------------------ PATCH ------------------ #

def test_patch_note():
    response = client.patch(f"/notes/{patchDeleteID}", headers=headers, json={"title": "New Title"})
    assert response.status_code == 200
    assert response.json()["updated_document"]["title"] == "New Title"

# ------------------ DELETE ------------------ #

def test_delete_note():
    response = client.delete(f"/{patchDeleteID}", headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Document deleted"

clear_test_collection()
