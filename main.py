from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "new World"}

@app.post("/createpost")
async def create_post():
    return {"message": "Post created successfully"}