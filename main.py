from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "new World"}

@app.post("/createpost")
async def create_post(payload : dict = Body(...)):
    print(payload)
    return {"Post created": "title: " + payload['title'] + "  content:  " + payload['content']}