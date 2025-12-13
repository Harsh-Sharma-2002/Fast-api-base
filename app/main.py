from fastapi import FastAPI,Response,status,HTTPException,Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
from utils import find_post, find_index_post
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session


app = FastAPI()

models.Base.metadata.create_all(bind = engine)

# my_posts = [{"title": "title of post 1", "content": "content of post 1","published": True, "rating": 5, "id": randrange(0,1000000)},
#             {"title": "title of post 2", "content": "content of post 2", "published": False, "rating": 4, "id": randrange(0,1000000)}]

###################################################################



###################################################################

# while(True):
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='new_password', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection was successful")
#         break
#     except Exception as error:
#         print("Connecting to database failed")
#         print("Error:", error)
#         time.sleep(2)


###################################################################
###################################################################

@app.get("/")
async def read_root():
    return {"Hello": "new World"}

###################################################################

@app.get("/posts")
def get_post(db: Session = Depends(get_db)):
    posts = db.query(models.PostModel).all()
    return {"data": posts}

###################################################################

@app.get("/posts/{id}",response_model = models.ResponsePost)
async def get_post(id: int,db: Session = Depends(get_db)): ## We take in id as int to avoid SQL injection
    #  cursor.execute("SELECT * FROM posts WHERE id = %s", (str(id),)) ## Used extra comma to make it a tuple
    #  cursor_post = cursor.fetchone()
    #  if not cursor_post:
    #      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                          detail=f"post with id: {id} was not found")
    post_id = db.query(models.PostModel).filter(models.PostModel.id == id).first()
    if not post_id:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"post with id: {id} was not found")
    return  post_id
  

###################################################################

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(new_post: models.CreatePost,db: Session = Depends(get_db)):
    # cursor.execute("INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *",
    #                (new_post.title, new_post.content, new_post.published))
    # created_post = cursor.fetchone()
    # conn.commit()
    new = models.PostModel(**new_post.dict())
    db.add(new)
    db.commit()
    db.refresh(new)
    return {"data": new}

###################################################################

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
#     cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (str(id),))
#     deleted_post = cursor.fetchone()
#     conn.commit()
#     if deleted_post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"post with id: {id} does not exist")
    to_delete_post = db.query(models.PostModel).filter(models.PostModel.id == id)
    if to_delete_post.first() == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"post with id: {id} does not exist")
    to_delete_post.delete(synchronize_session=False)
    db.commit()

#     return Response(status_code=status.HTTP_204_NO_CONTENT)

###################################################################

@app.put("/posts/{id}",response_model = models.ResponsePost)
def update_post(id: int, updated_post: models.UpdatePost, db: Session = Depends(get_db)):
#     cursor.execute("UPDATE posts SET title = %s,content = %s,published = %s WHERE id = %s RETURNING *",
#                    (updated_post.title, updated_post.content, updated_post.published, str(id)))
#     updated_cursor_post = cursor.fetchone()
#     conn.commit()
#     if updated_cursor_post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"post with id: {id} does not exist")
    post_query = db.query(models.PostModel).filter(models.PostModel.id == id)
    post_up = post_query.first()
    if post_up == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"post with id: {id} does not exist")
    post_query.update(updated_post.dict(exclude_unset=True),synchronize_session=False)
    db.commit()
    db.refresh(post_up)

    return post_up
       
 