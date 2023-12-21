from fastapi import FastAPI
from enum import Enum

#str tells the parameter will be string
#enum enumerates the model_name as "model_name.alexnet", "model_name.cnn", "model_name.lstm" Enum is the base class

class model_name(str,Enum):
    alexnet = "alexnet"
    cnn = "cnn"
    lstm = "lstm"



#app is an instance of FastAPI
app = FastAPI()

#Decorator is being used, a function is wrapped around another function
#inner function is passed as arg to the @func
#url gives us the parameter in {x} that is then used in the inner function

@app.get("/subject/{x}")
async def choose_subject(x: model_name): #x: model_name shows that the path parameter is of the type class model_name
    if x is model_name.alexnet: #x is the class name, x.value will give its value, if x.value = alexnet
        return "alexnet"
    elif x is model_name.cnn:
        return "cnn"
    elif x is model_name.lstm:
        return "lstm" 