from pydantic import BaseModel

class book_body(BaseModel):
    name: str
    price: float

    class Config:
        orm_model = True