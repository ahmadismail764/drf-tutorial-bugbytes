from fastapi import FastAPI
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine
from .routers import post, user, auth
 
models.Base.metadata.create_all(bind=engine) # type: ignore

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host='localhost',
        database='fastapi',
        user='postgres',
        password='POSTGRES_PASSWORD123',
        cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection succesful")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error:", error)
        time.sleep(2)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Hello World"}