from sqlalchemy import Column, Float, Integer, String, Boolean 

from database import Base

class book_body(Base):
    __tablename__ = "library"

    id = Column(Integer,primary_key = True, index = True)
    name = Column(String, index = True)
    price = Column(Float, index = True)



#------------------------------------------ Auth ------------------------------------------#

class UserInDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True, unique=True)
    email = Column(String, index=True, nullable=True)
    full_name = Column(String, nullable=True)
    hashed_password = Column(String)
    disabled = Column(Boolean, default=False)

class Token(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True, index=True)
    access_token = Column(String, index=True)
    token_type = Column(String)
