from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
from utils import find_post, find_index_post
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

my_posts = [{"title": "title of post 1", "content": "content of post 1","published": True, "rating": 5, "id": randrange(0,1000000)},
            {"title": "title of post 2", "content": "content of post 2", "published": False, "rating": 4, "id": randrange(0,1000000)}]

###################################################################

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

###################################################################

while(True):
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='new_password', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error:", error)
        time.sleep(2)

###################################################################
class UpdatePost(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    published: Optional[bool] = None
    rating: Optional[int] = None


###################################################################

@app.get("/")
async def read_root():
    return {"Hello": "new World"}

###################################################################

@app.get("/posts")
async def get_post():
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    return {"data": posts}

###################################################################

@app.get("/posts/{id}")
async def get_post(id: int, Response: Response):
    cursor.execute("SELECT * FROM posts WHERE id = {id}".format(id=id))
    cursor_post = cursor.fetchone()
    if not cursor_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return {"post_details": cursor_post}
  

###################################################################

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(new_post: Post):
    cursor.execute("INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *",
                   (new_post.title, new_post.content, new_post.published))
    created_post = cursor.fetchone()
    conn.commit()
    return {"data": created_post}

###################################################################

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    post = find_post(id, my_posts)
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    my_posts.remove(post)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

###################################################################

@app.put("/posts/{id}")
def update_post(id: int, updated_post: UpdatePost):
    index = find_index_post(id,my_posts)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    my_posts[index].update(updated_post.dict(exclude_unset=True))
    return {"data": my_posts[index]}
 