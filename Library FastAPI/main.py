from fastapi import FastAPI
import models, schemas
from database import engine
from sqlalchemy.orm import Session
from dependency import get_db
models.Base.metadata.create_all(bind=engine)


app = FastAPI()




@app.get()
def HomePage():
    return {"Welcome to the Library"}


