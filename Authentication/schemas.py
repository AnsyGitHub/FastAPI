from pydantic import BaseModel

class book_body(BaseModel):
    name: str
    price: float

    class Config:
        orm_model = True

#--------------------------------------Authentication and JWT -----------------------------------------#
        
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
