# app/api/api_v1/endpoints/users.py
from fastapi import APIRouter, Depends
from app.core.authentication import get_current_user
from app.schemas.user import UserTokenData

router = APIRouter()


@router.get("/")
def read_item(user: UserTokenData = Depends(get_current_user)):
    return [{"item1": "Foo"}, {"item2": "Bar"}]
