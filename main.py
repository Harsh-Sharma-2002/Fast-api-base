from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

my_posts = [{"title": "title of post 1", "content": "content of post 1","published": True, "rating": 5, "id": 1},
            {"title": "title of post 2", "content": "content of post 2", "published": False, "rating": 4, "id": 2}]

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

@app.post("/posts")
async def create_post(new_post: Post):
    print(new_post.dict())
    dict_temp = new_post.dict()
    dict_temp['id'] = len(my_posts) + 1
    my_posts.append(dict_temp)
    return {"Data": "new_post"}
