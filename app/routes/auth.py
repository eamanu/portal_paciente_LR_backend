from datetime import timedelta
from enum import Enum

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.auth.auth import authenticate_user, authenticate_user_and_is_admin
from app.auth.auth import create_access_token
from app.auth.auth import get_user
from app.config.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.gear.local.local_impl import LocalImpl
from app.main import get_db
from app.schemas.person import PersonLogged


class ID_PERSON_STATUS(Enum):
    NOT_VALIDATED_YET = 1
    VALIDATED = 2


class ID_ADMIN_STATUS(Enum):
    NOT_VALIDATED_YET = 1
    VALIDATED = 2
    REFUSED = 3


def login_for_access_token(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    username = form_data.username
    user = authenticate_user_and_is_admin(db, username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


def login_person(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):

    username = form_data.username
    is_authorized = authenticate_user(db, username, form_data.password)
    if not is_authorized:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password...",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": username}, expires_delta=access_token_expires
    )

    # 1. Query para traer Person y Familia
    user = get_user(username)
    family_boss = LocalImpl().get_person_by_id(user.id_person)

    # 2. Check si esa Persona ya valido email
    if family_boss.id_person_status != ID_PERSON_STATUS.VALIDATED.value:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Mail not validated."
        )

    # 3. Check si fue aprobado por el admin
    if family_boss.id_admin_status != ID_ADMIN_STATUS.VALIDATED.value:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wait for approval."
        )

    return PersonLogged(
        id_person=user.id_person,
        access_token=access_token,
        token_type="bearer",
        data=family_boss)
