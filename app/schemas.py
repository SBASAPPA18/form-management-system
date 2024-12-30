from pydantic import BaseModel, EmailStr
from typing import List, Optional, Union
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str

class FormField(BaseModel):
    field_id: str
    type: str  # "string", "number", "boolean"
    label: str
    required: bool

class FormCreate(BaseModel):
    title: str
    description: str
    fields: List[FormField]

class FormResponse(FormCreate):
    id: int
    creator_id: int

class FormSubmissionCreate(BaseModel):
    responses: List[dict]

class FormSubmissionResponse(BaseModel):
    submission_id: str
    submitted_at: datetime
    data: dict