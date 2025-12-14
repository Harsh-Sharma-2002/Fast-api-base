
from typing import List
from . import models
from . import schema, utils
from .database import engine, get_db
from fastapi import FastAPI
from .routers import post, users


models.Base.metadata.create_all(bind = engine)




app = FastAPI()

app.include_router(post.router)
app.include_router(users.router)

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

@app.get("/")
async def read_root():
    return {"Hello": "new World"}






