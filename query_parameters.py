from fastapi import FastAPI

nd = FastAPI()



#q is the query parameter, FastAPI can differentiate between path parameter and query parameter
#q can either be a string or be None by default

#URL/items/5?q=3
#where 5 is the item_id and after ? is the query parameter
#it can be given more parameters by using &, such as #URL/items/5?q=3&p=5 
 
@nd.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}