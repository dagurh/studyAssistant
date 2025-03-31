from typing import Union, Annotated
import time

from fastapi import FastAPI, Query, Request, Depends, HTTPException, status
from database import insertIntoDB, queryDB, deleteFromDB,  updateDB
from openaiAPI import generate_test_from_notes, generate_summary_from_notes
from jsonPayload import practice_test_payload, summary_payload
from models.models import Course, Note, NoteFilter, CourseFilter, NoteUpdate

app = FastAPI()

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

@app.get("/")
def read_root():
    return {"Head over to /docs for API documentation"}

@app.get("/courses/", status_code=200)
async def getCourses(courseFilter: CourseFilter = Depends()):
    filter_dict = courseFilter.filter_dict()
    result = await queryDB(filter_dict)
    return {"message": "Query successful", "courses": result}

@app.get("/notes/", status_code=200)
async def getNotes(noteFilter: NoteFilter = Depends()):
    filter_dict = noteFilter.filter_dict()
    result = await queryDB(filter_dict)
    return {"message": "Query successful", "notes": result}

@app.get("/summaries/", status_code=200)
async def getNotes():
    # TODO: Implement this endpoint to return summaries
    return {"GET summaries called"}

@app.get("/practicetests/", status_code=200)
async def getNotes():
    # TODO: Implement this endpoint to return practice tests
    return {"GET practicetests called"}



@app.post("/courses", status_code=201)
async def postCourses(course_data: Course):

    doc = course_data.model_dump()
    await insertIntoDB(doc)
    doc["_id"] = str(doc["_id"])
    return {"message": "Course added successfully", "course": doc}

@app.post("/notes", status_code=201)
async def postNotes(note: Note):
    
    note_dict = note.model_dump()
    await insertIntoDB(note_dict)
    note_dict["_id"] = str(note_dict["_id"])
    return {"message": "Note added successfully", "note": note_dict}

@app.post("/practicetests", status_code=201)
async def generate_practicetests(
    noteFilter: NoteFilter,
    num_questions: int = Query(5, ge=1, le=10)
    ):

    filter_dict = noteFilter.filter_dict()

    result = await queryDB(filter_dict)

    texts = [note["text"] for note in result]

    questions = generate_test_from_notes(texts, num_questions)
    payload = practice_test_payload(filter_dict, questions)

    await insertIntoDB(payload)

    payload["_id"] = str(payload["_id"])

    return {"message": "Query successful", "inserted": payload}

@app.post("/summaries", status_code=201)
async def generate_summaries(noteFilter: NoteFilter):
    filter_dict = noteFilter.filter_dict()

    result = await queryDB(filter_dict)

    texts = [note["text"] for note in result]

    summary = generate_summary_from_notes(texts)
    payload = summary_payload(filter_dict, summary)

    await insertIntoDB(payload)

    payload["_id"] = str(payload["_id"])

    return {"message": "Query successful", "inserted": payload}

@app.patch("/courses/{id}", status_code=200)
async def patchNotes(id: str, course: Course):
    course_dict = course.model_dump()
    result, status_code = await updateDB(id, course_dict)

    if status_code == 400:
        raise HTTPException(status_code=400, detail=result["message"])
    if status_code == 404:
        raise HTTPException(status_code=404, detail=result["message"])
    return result

@app.patch("/notes/{id}", status_code=200)
async def patchNotes(id: str, noteUpdate: NoteUpdate):
    note_dict = noteUpdate.filter_dict()
    result, status_code = await updateDB(id, note_dict)

    if status_code == 400:
        raise HTTPException(status_code=400, detail=result["message"])
    if status_code == 404:
        raise HTTPException(status_code=404, detail=result["message"])
    return result

@app.delete("/{id}")
async def delete_note(id: str):
    result, status_code = await deleteFromDB(id)

    if status_code == 400:
        raise HTTPException(status_code=400, detail=result["message"])
    if status_code == 404:
        raise HTTPException(status_code=404, detail=result["message"])

    return result
