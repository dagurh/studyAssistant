from pydantic import BaseModel
from typing import Literal, Optional, Union, Annotated
from fastapi import Query

class FilterBaseModel(BaseModel):
    def filter_dict(self):
        return {k: v for k, v in self.model_dump().items() if v is not None}

class Course(BaseModel):
    type: Literal["course"] = "course"
    course: str
    title: str

class CourseFilter(FilterBaseModel):
    type: Literal["course"] = "course"
    course: Annotated[Optional[str], Query(min_length=6, max_length=7)] = None
    title: Annotated[Optional[str], Query(min_length=3, max_length=30)] = None

class Note(BaseModel):
    type: Literal["note"] = "note"
    title: Union[str, None] = None
    course: Annotated[Union[str, None], Query(min_length=6, max_length=7)] = None
    chapter: Union[int, None] = None
    text: Annotated[str, Query(min_length=10)]

class NoteFilter(FilterBaseModel):
    type: Literal["note"] = "note"
    course: Optional[str] = None
    title: Optional[str] = None
    chapter: Optional[int] = None

class NoteUpdate(FilterBaseModel):
    type: Literal["note"] = "note"
    course: Optional[str] = None
    title: Optional[str] = None
    chapter: Optional[int] = None
    text: Optional[str] = None

class SummaryFilter(FilterBaseModel):
    type: Literal["summary"] = "summary"
    course: Optional[str] = None
    title: Optional[str] = None
    chapter: Optional[int] = None

class PracticeTestFilter(FilterBaseModel):
    type: Literal["practice_test"] = "practice_test"
    course: Optional[str] = None
    title: Optional[str] = None
    chapter: Optional[int] = None