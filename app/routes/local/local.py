from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.main import get_db
from app.routes import auth
from app.routes.common import router_local
from app.schemas.token import Token

@router_local.post("/login", response_model=Token)
async def login_for_access_token(db: Session = Depends(get_db),
                                 form_data: OAuth2PasswordRequestForm = Depends()):
    return auth.login_for_access_token(db, form_data)


@router_local.post("/logout")
async def logout(token: Token):

    print(token)
    pass