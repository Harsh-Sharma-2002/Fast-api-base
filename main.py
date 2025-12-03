from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
from utils import find_post

app = FastAPI()

my_posts = [{"title": "title of post 1", "content": "content of post 1","published": True, "rating": 5, "id": randrange(0,1000000)},
            {"title": "title of post 2", "content": "content of post 2", "published": False, "rating": 4, "id": randrange(0,1000000)}]

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


@app.get("/")
async def read_root():
    return {"Hello": "new World"}

@app.get("/posts")
async def get_post():
    return {"data": my_posts}

@app.get("/posts/{id}")
async def get_post(id: int, Response: Response):
    post = find_post(id, my_posts)
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return {"post_details": post}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(new_post: Post):
    dict_temp = new_post.dict()
    dict_temp['id'] = randrange(0, 1000000)
    my_posts.append(dict_temp)
    return {"Data": dict_temp}

@app.delete("/posts/{id}")
def delete_post(id: int):
    post = find_post(id, my_posts)
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    my_posts.remove(post)
    return {"message": "post deleted successfully"}