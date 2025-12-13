from pydantic import BaseModel, EmailStr
from typing import Optional,List
from datetime import datetime


class CreatePost(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True

class ResponsePost(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    created_at: datetime

    class Config:
        orm_mode = True # to work with sqlalchemy models fastapi works with.pydantic models so this will help in converting sqlalchemy model to pydantic model and sqlalchemy mdoel is python class so this will help in converting it to dict and then to json

     
class UpdatePost(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    published: Optional[bool] = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True