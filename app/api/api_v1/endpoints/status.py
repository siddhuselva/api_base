# api/api_v1/endpoints/status.py
from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def get_status():
    return {"status": "OK"}
