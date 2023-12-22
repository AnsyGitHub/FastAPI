from fastapi import FastAPI, Path, HTTPException
import os
import json
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder

app = FastAPI()

#Pydantic Class as a parent
class book_body(BaseModel):
    name: str
    price: float

#JSON file to replicate DB
BOOKS = "bookfile.json"
BOOK_DB = []

#if path exists, fill the global array BOOK_DB with data
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
    book_json = jsonable_encoder(book) #Pydantic class was not JSON serializeable, hence the encoding
    BOOK_DB.append(book_json)
    with open(BOOKS,'w') as f:
        json.dump(BOOK_DB,f)
    return {"message" : f"The book {book} has been added"}

@app.put("/get-by-id/{random_id}")
async def updatebook(random_id: int, book:book_body):
    book_encoded = jsonable_encoder(book)
    BOOK_DB[random_id-1] = book_encoded
    with open(BOOKS,'w') as f:
        json.dump(BOOK_DB,f)
    return {"message" : f'The id {random_id} book {book.name} has been updated'}

@app.delete("/get-by-id/{random_id}")
async def deletion(random_id: int):
    del BOOK_DB[random_id-1]
    with open(BOOKS,'w') as f:
        json.dump(BOOKS,f)
    return {f'The requested book no. {random_id} has been deleted'}




