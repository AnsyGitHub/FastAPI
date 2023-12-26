from sqlalchemy import Column, Float, Integer, String

from database import Base

class book_body(Base):
    __tablename__ = "library"

    id = Column(Integer,primary_key = True, index = True)
    name = Column(String, index = True)
    price = Column(Float, index = True)

