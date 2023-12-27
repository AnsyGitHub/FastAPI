from pydantic import BaseModel

class UserLogin(BaseModel):
    username: str
    password: str

class BookCreate(BaseModel):
    title: str
    author: str
    ISBN: str

class MemberCreate(BaseModel):
    name: str
    email: str
    membership_id: str

class BorrowRecordCreate(BaseModel):
    member_id: int
    book_id: int

class BorrowRecordReturn(BaseModel):
    return_date: str  


#----------------------------------------------#
    
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str
