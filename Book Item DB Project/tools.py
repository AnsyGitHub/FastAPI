from sqlalchemy.orm import Session
import models, schemas
from sqlalchemy import update


def get_book(db: Session, user_id: int):
    return db.query(models.book_body).filter(models.book_body.id == user_id).first()


def get_book_by_name(db: Session, name: str):
    return db.query(models.book_body).filter(models.book_body.name == name).first()


def get_books(db: Session):
    return db.query(models.book_body).all()


def get_books_names(db: Session):
    book_names = []
    for naming in db.query(models.book_body.name).all():
        book_names.append(naming[0]) 
    return book_names

def create_book(db: Session, book: schemas.book_body):
    db_book = models.book_body(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def delete_book(db:Session, id: int):
    db.query(models.book_body).filter(models.book_body.id == id).delete()
    db.commit()

def update_record(db:Session, id:int, new_data: schemas.book_body):
    stmt = update(models.book_body).where(models.book_body.id == id).values(**new_data.model_dump())
    result = db.execute(stmt)
    db.commit()
    return "Updated"


