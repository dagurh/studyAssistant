from typing import Union, Annotated
import time

from fastapi import FastAPI, Query, Request
from pydantic import BaseModel
from database import insertIntoDB, queryDB

app = FastAPI()

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
async def read_item(
    item_id: int, 
    q: Annotated[Union[str, None], Query(min_length=3, max_length=50)] = None
):
    return {"item_id": item_id, "q": q}

@app.put("/items/{item_id}")
async def update_item(
    item_id: int, 
    item: Item
):
    return {"item_price": item.price, "item_id": item_id}

@app.get("/courses/", status_code=200)
async def getCourses(
    course: Annotated[Union[str, None], Query(min_length=6, max_length=7)] = None
):
    doc = {}
    if course == None:
        doc = { "course": {"$exists": True}, "title": {"$exists": True} }
    else:
        doc = { "course": course }

    result = await queryDB(doc)
    return result

@app.get("/notes/", status_code=200)
async def getNotes():
    return {"GET notes called"}

@app.get("/summaries/", status_code=200)
async def getNotes():
    return {"GET summaries called"}

@app.get("/practicetests/", status_code=200)
async def getNotes():
    return {"GET practicetests called"}



@app.post("/courses", status_code=201)
async def postCourses(
    course: str,
    title: str
):
    doc = { "course": course, "title": title }
    await insertIntoDB(doc)
    return {"POST courses called"}

@app.post("/notes", status_code=201)
async def postNotes():
    return {"POST notes called"}



@app.patch("/courses", status_code=200)
async def patchCourses():
    return {"PATCH courses called"}

@app.patch("/notes", status_code=200)
async def patchNotes():
    return {"PATCH notes called"}



@app.delete("/courses", status_code=204)
async def deleteCourses():
    return {"DELETE courses called"}

@app.delete("/notes", status_code=204)
async def deleteNotes():
    return {"DELETE notes called"}

@app.delete("/summaries", status_code=204)
async def deleteNotes():
    return {"DELETE summaries called"}

@app.delete("/practicetests", status_code=204)
async def deleteNotes():
    return {"DELETE practicetests called"}