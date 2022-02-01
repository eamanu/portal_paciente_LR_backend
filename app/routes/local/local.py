from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from app.config.config import SECRET_KEY, ALGORITHM
from app.main import get_db
from app.gear.local.local_impl import Local_Impl
from app.routes import auth
from app.routes.common import router_local
from app.schemas.token import Token
from app.schemas.user import User as schema_user


@router_local.post("/login", response_model=Token)
async def login_for_access_token(db: Session = Depends(get_db),
                                 form_data: OAuth2PasswordRequestForm = Depends()):
    return auth.login_for_access_token(db, form_data)


@router_local.post("/logout")
async def logout(token: Token):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token.access_token, SECRET_KEY, algorithms=[ALGORITHM])

        expires = datetime.fromtimestamp(payload.get("exp"))

        if expires is None:
            raise credentials_exception

        Local_Impl().set_expiration_black_list(token)

    except JWTError:
        raise credentials_exception


@router_local.post("/createuser")
async def create_user(user: schema_user):
    return Local_Impl().create_user(user)