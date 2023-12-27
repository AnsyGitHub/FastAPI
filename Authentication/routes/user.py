from fastapi import APIRouter, Depends
from typing import Annotated
from dependency import get_current_active_user
import schemas

router = APIRouter(prefix= "/users/me",tags=["users"])



@router.get("/")
async def read_users_me(current_user: Annotated[schemas.User, Depends(get_current_active_user)]):
    return current_user

@router.get("/items")
async def read_own_items(current_user: Annotated[schemas.User, Depends(get_current_active_user)]):
    return [{"item_id": "Foo", "owner": current_user.username}]


