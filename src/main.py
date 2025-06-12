from typing import Union, Annotated
import time

from fastapi import FastAPI, Query, Request, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from src.database import insertIntoDB, queryDB, deleteFromDB,  updateDB, getUserByEmail, saveUser
from src.openaiAPI import generate_test_from_notes, generate_summary_from_notes
from src.jsonPayload import practice_test_payload, summary_payload
from src.models.models import Course, Note, NoteFilter, CourseFilter, NoteUpdate, SummaryFilter, PracticeTestFilter, NoteTests, UserCreate, UserLogin
from src.auth.utils import hash_password, verify_password, create_access_token
from src.auth.protected import get_current_user
from datetime import timedelta

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or ["*"] for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

@app.post("/register", status_code=201)
async def register_user(user: UserCreate):
    existing_user = await getUserByEmail(user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = hash_password(user.password)
    user_dict = user.model_dump()
    await saveUser({ "email": user_dict["email"], "hashed_password": hashed_password })
    return {"message": "User registered successfully"}

@app.post("/login", status_code=200)
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await getUserByEmail(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": user["email"]}, expires_delta=timedelta(minutes=30))
    return {"access_token": access_token, "token_type": "bearer"}



#GET requests

@app.get("/")
def read_root():
    return {"Head over to /docs for API documentation"}

@app.get("/courses/", status_code=200)
async def getCourses(courseFilter: CourseFilter = Depends(), user = Depends(get_current_user)):
    filter_dict = courseFilter.filter_dict()
    filter_dict["user"] = user["email"]
    result = await queryDB(filter_dict)

    if result == []:
        return {"message": "No courses found for the given filter"}

    return {"message": "Query successful", "courses": result}

@app.get("/notes/", status_code=200)
async def getNotes(noteFilter: NoteFilter = Depends(), user = Depends(get_current_user)):
    filter_dict = noteFilter.filter_dict()
    filter_dict["user"] = user["email"]
    result = await queryDB(filter_dict)

    if result == []:
        return {"message": "No notes found for the given filter"}

    return {"message": "Query successful", "notes": result}

@app.get("/summaries/", status_code=200)
async def getSummaries(summaryFilter: SummaryFilter = Depends(), user = Depends(get_current_user)):
    filter_dict = summaryFilter.filter_dict()
    filter_dict["user"] = user["email"]
    result = await queryDB(filter_dict)

    if result == []:
        return {"message": "No summaries found for the given filter"}
    
    return {"message": "Query successful", "summaries": result}

@app.get("/practicetests/", status_code=200)
async def getPracticeTests(practiceTestFilter: PracticeTestFilter = Depends(), user = Depends(get_current_user)):
    filter_dict = practiceTestFilter.filter_dict()
    filter_dict["user"] = user["email"]
    result = await queryDB(filter_dict)

    if result == []:
        return {"message": "No practice tests found for the given filter"}
    
    return {"message": "Query successful", "practicetests": result}

#POST requests

@app.post("/courses", status_code=201)
async def postCourses(course_data: Course, user = Depends(get_current_user)):

    doc = course_data.model_dump()
    doc["user"] = user["email"]
    await insertIntoDB(doc)
    return {"message": "Course added successfully", "course": doc}

@app.post("/notes", status_code=201)
async def postNotes(note: Note, user = Depends(get_current_user)):
    
    note_dict = note.model_dump()
    note_dict["user"] = user["email"]
    await insertIntoDB(note_dict)
    #note_dict["_id"] = str(note_dict["_id"])
    return {"message": "Note added successfully", "note": note_dict}

@app.post("/practicetests", status_code=201)
async def generate_practicetests(
    noteTests: NoteTests,
    num_questions: int = Query(5, ge=1, le=10),
    user = Depends(get_current_user)
    ):

    filter_dict = noteTests.filter_dict()
    filter_dict["user"] = user["email"]

    result = await queryDB(filter_dict)

    if result == []:
        raise HTTPException(status_code=404, detail="No notes found for the given filter")

    texts = [note["text"] for note in result]

    questions = generate_test_from_notes(texts, num_questions)
    payload = practice_test_payload(filter_dict, questions)

    await insertIntoDB(payload)

    #payload["_id"] = str(payload["_id"])

    return {"message": "Query successful", "inserted": payload}

@app.post("/summaries", status_code=201)
async def generate_summaries(noteFilter: NoteFilter, user = Depends(get_current_user)):
    filter_dict = noteFilter.filter_dict()
    filter_dict["user"] = user["email"]

    result = await queryDB(filter_dict)

    if result == []:
        raise HTTPException(status_code=404, detail="No notes found for the given filter")

    texts = [note["text"] for note in result]

    summary = generate_summary_from_notes(texts)
    payload = summary_payload(filter_dict, summary)

    await insertIntoDB(payload)

    #payload["_id"] = str(payload["_id"])

    return {"message": "Query successful", "inserted": payload}

#PATCH requests

@app.patch("/courses/{id}", status_code=200)
async def patchNotes(id: str, course: Course, user = Depends(get_current_user)):
    course_dict = course.model_dump()
    course_dict["user"] = user["email"]
    result, status_code = await updateDB(id, course_dict)

    if status_code == 400:
        raise HTTPException(status_code=400, detail=result["message"])
    if status_code == 404:
        raise HTTPException(status_code=404, detail=result["message"])
    return result

@app.patch("/notes/{id}", status_code=200)
async def patchNotes(id: str, noteUpdate: NoteUpdate, user = Depends(get_current_user)):
    note_dict = noteUpdate.filter_dict()
    note_dict["user"] = user["email"]
    result, status_code = await updateDB(id, note_dict)

    if status_code == 400:
        raise HTTPException(status_code=400, detail=result["message"])
    if status_code == 404:
        raise HTTPException(status_code=404, detail=result["message"])
    return result

#DELETE requests

@app.delete("/{id}")
async def delete_note(id: str, user = Depends(get_current_user)):
    userEmail = user["email"]
    result, status_code = await deleteFromDB(id, userEmail)

    if status_code == 400:
        raise HTTPException(status_code=400, detail=result["message"])
    if status_code == 404:
        raise HTTPException(status_code=404, detail=result["message"])

    return result
