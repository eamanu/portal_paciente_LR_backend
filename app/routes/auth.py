#from fastapi import APIRouter
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.auth.auth import authenticate_user
from app.config.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.main import get_db
#from app.schemas.token import Token
from datetime import timedelta
from app.auth.auth import create_access_token
#from app.routes.common import router_local

#router = APIRouter(
#    prefix="", tags=["auth"], responses={404: {"description": "Not Found"}}
#)


#@router_local.post("/login", response_model=Token)
def login_for_access_token(db: Session = Depends(get_db),
                                 form_data: OAuth2PasswordRequestForm = Depends()):

    username = form_data.username
    user = authenticate_user(db, username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}