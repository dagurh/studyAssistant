from pydantic import BaseModel, ConfigDict, Field, EmailStr
from typing import Literal, Optional
from fastapi import Query

class StrictBaseModel(BaseModel):
    model_config = ConfigDict(extra='forbid')

class FilterBaseModel(StrictBaseModel):
    def filter_dict(self):
        return {k: v for k, v in self.model_dump().items() if v is not None}

class Course(StrictBaseModel):
    type: Literal["course"] = "course"
    course: str = Field(
        min_length=6, 
        max_length=7
        )
    title: Optional[str] = Field(
        default=None,
        min_length=3, 
        max_length=30
        )
    description: Optional[str] = Field(
        default=None,
        min_length=10, 
        max_length=300
        )
    credits: Optional[int] = Field(
        default=None,
        ge=0, 
        le=30
        )

class CourseFilter(FilterBaseModel):
    type: Literal["course"] = "course"
    course: Optional[str] = Query(
        default=None,
        min_length=6, 
        max_length=7
        )
    title: Optional[str] = Query(
        default=None,
        min_length=3,
        max_length=30
        )
    credits: Optional[int] = Query(
        default=None,
        ge=0, 
        le=30
        )

class Note(StrictBaseModel):
    type: Literal["note"] = "note"
    title: Optional[str] = Field(
        default=None,
        min_length=3, 
        max_length=30
        )
    course: str = Field(
        min_length=6, 
        max_length=7
        )
    chapter: Optional[int] = Field(
        default=None,
        ge=0, 
        le=100
        )
    text: str = Field(
        min_length=20, 
        max_length=5000
        )

class NoteFilter(FilterBaseModel):
    type: Literal["note"] = "note"
    title: Optional[str] = Query(
        default=None,
        min_length=3, 
        max_length=30
        )
    course: Optional[str] = Query(
        default=None,
        min_length=6, 
        max_length=7
        )
    chapter: Optional[int] = Query(
        default=None,
        ge=0,
        le=100
        )
    
class NoteTests(FilterBaseModel):
    type: Literal["note"] = "note"
    title: Optional[str] = Field(
        default=None,
        min_length=3, 
        max_length=30
        )
    course: Optional[str] = Field(
        default=None,
        min_length=6, 
        max_length=7
        )
    chapter: Optional[int] = Field(
        default=None,
        ge=0,
        le=100
        )

class NoteUpdate(FilterBaseModel):
    type: Literal["note"] = "note"
    course: Optional[str] = Field(
        default=None,
        min_length=6, 
        max_length=7
        )
    title: Optional[str] = Field(
        default=None,
        min_length=3, 
        max_length=30
        )
    chapter: Optional[int] = Field(
        default=None,
        ge=0, 
        le=100
        )
    text: Optional[str] = Field(
        default=None,
        min_length=20, 
        max_length=5000
        )

class SummaryFilter(FilterBaseModel):
    type: Literal["summary"] = "summary"
    course: Optional[str] = Field(
        default=None,
        min_length=6, 
        max_length=7
        )
    title: Optional[str] = Field(
        default=None,
        min_length=3, 
        max_length=30
        )
    chapter: Optional[int] = Field(
        default=None,
        ge=0, 
        le=100
        )
    
class PracticeTestFilter(FilterBaseModel):
    type: Literal["practice_test"] = "practice_test"
    course: Optional[str] = Field(
        default=None,
        min_length=6, 
        max_length=7
        )
    title: Optional[str] = Field(
        default=None,
        min_length=3, 
        max_length=30
        )
    chapter: Optional[int] = Field(
        default=None,
        ge=0, 
        le=100
        )
    
class UserCreate(StrictBaseModel):
    email: EmailStr = Field(
        min_length=5, 
        max_length=50
        )
    password: str = Field(
        min_length=8, 
        max_length=100
        )
    
class UserLogin(BaseModel):
    email: EmailStr = Field(
        min_length=5, 
        max_length=50
        )
    password: str = Field(
        min_length=8, 
        max_length=100
        )
    
class UserInDB(UserCreate):
    hashed_password: str = Field(
        min_length=8, 
        max_length=100
        )
    