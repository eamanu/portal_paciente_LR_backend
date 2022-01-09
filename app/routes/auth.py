from typing import Dict

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.auth.auth import login
from app.main import get_db
from app.schemas import AccessToken

router = APIRouter(
    prefix="/auth", tags=["auth"], responses={404: {"description": "Not Found"}}
)


@router.post("/", response_model=AccessToken)
async def auth(user_id: str, password: str, db: Session = Depends(get_db)) -> Dict:
    if login(db, user_id, password):
        return {"access_token": "True"}
    return {"access_token": "Error authentication"}
