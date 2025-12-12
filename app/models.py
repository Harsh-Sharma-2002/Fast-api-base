from .database import Base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PostModel(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)

    published = Column(Boolean, server_default=text("TRUE"), nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )


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
        orm_mode = True

     

class UpdatePost(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    published: Optional[bool] = True
 
  

