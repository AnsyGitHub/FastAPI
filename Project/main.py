from fastapi import FastAPI, Path, HTTPException
import os
import json
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder

app = FastAPI()

class book_body(BaseModel):
    name: str
    price: float

BOOKS = "bookfile.json"
BOOK_DB = []

if os.path.exists(BOOKS):
    with open(BOOKS, 'r') as f:
        BOOK_DB = json.load(f)

@app.get("/")
async def homepage():
    return {"Welcome to my book store"}

@app.get("/list-books")
async def listbooks():
    return {"Books" : BOOK_DB}

@app.get("/get-by-id/{random_id}")
async def getbook(random_id: int):
    check = len(BOOK_DB)
    if random_id <= 0 or random_id > check:
        raise HTTPException(404, "You are adding wrong index")
    return BOOK_DB[random_id-1]

@app.post("/add_book")
async def addBook(book: book_body):
    book_json = jsonable_encoder(book)
    BOOK_DB.append(book_json)
    with open(BOOKS,'w') as f:
        json.dump(BOOK_DB,f)
    return {"message" : f"The book {book} has been added"}



