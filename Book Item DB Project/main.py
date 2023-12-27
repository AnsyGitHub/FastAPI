from fastapi import FastAPI, Depends

from database import engine, SessionLocal, Base
import models, schemas, tools

from sqlalchemy.orm import Session



models.Base.metadata.create_all(bind=engine)


app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def homepage():
    return {"Welcome to my book store"}

@app.get("/list-books")
async def listbooks(db: Session = Depends(get_db)):
    return tools.get_books(db)

@app.get("/get-by-id/{random_id}")
async def getbook(random_id: int, db: Session = Depends(get_db)):
    return tools.get_book(db, random_id)    #db.query(models.book_body).filter(models.book_body.id == random_id).first()

@app.post("/add_book")
async def addBook(book: schemas.book_body,db: Session = Depends(get_db)):
    return tools.create_book(db, book)

@app.get("/names")
async def displayNames(db: Session = Depends(get_db)):
    return tools.get_books_names(db)


@app.put("/update-name/{random_id}")
async def updatebook(random_id: int, book:schemas.book_body, db: Session = Depends(get_db)):
    return tools.update_record(db,random_id,book)

@app.delete("/deleteID/{random_id}")
async def deletion(random_id: int, db: Session = Depends(get_db)):
    return tools.delete_book(db,random_id)