from fastapi import FastAPI, Depends, APIRouter

from database import engine, SessionLocal, Base
import models, schemas, tools

from sqlalchemy.orm import Session
# from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from routes import user
from dependency import get_db, get_current_active_user

SECRET_KEY = "a652a9b7fd648256b983af18f2e8e4e5ad48dd7c99c9c89dc1c5217f6ec5bca7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")




models.Base.metadata.create_all(bind=engine)
#-----------------------------------------------------------------------------------------------------------------------#




def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)

def get_username(username: str, db: Session = Depends(get_db)):
    return db.query(models.UserInDB).filter(models.UserInDB.username == username).first()


# Function to authenticate user
def authenticate_user(username: str, password: str, db: Session = Depends(get_db)):
    user = get_username(username,db)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user    

def create_access_token(data: dict, expires_delta: timedelta | None = None, db: Session = Depends(get_db)):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


app = FastAPI()
app.include_router(user.router)

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires, db=db
    )
    return {"access_token": access_token, "token_type": "bearer"}




@app.get("/")
async def homepage(current_user: Annotated[schemas.User, Depends(get_current_active_user)]):
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
async def updatebook(random_id: int, book:schemas.book_body, current_user: Annotated[schemas.User, Depends(get_current_active_user)], db: Session = Depends(get_db)):
    tools.update_record(db,random_id,book)
    return {"By owner: " + current_user}

@app.delete("/deleteID/{random_id}")
async def deletion(random_id: int, db: Session = Depends(get_db)):
    return tools.delete_book(db,random_id)

@app.put("/User")
async def create_user_auth(user:schemas.User,password:str, db: Session = Depends(get_db)):
    hp = get_password_hash(password)
    new_user = schemas.UserInDB(**user.model_dump(), hashed_password= hp)
    db_user = models.UserInDB(**new_user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return "User Added"

