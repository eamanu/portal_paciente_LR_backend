from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.auth.auth import authenticate_user
from app.config.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.main import get_db
from datetime import timedelta
from app.auth.auth import create_access_token
from app.auth.auth import get_user
from app.gear.local.local_impl import LocalImpl
from app.schemas.person import PersonLogged


def login_for_access_token(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
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


def login_person(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):

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

    # 1. Query para traer Person
    # 2. Check Si esa Person es el "jefe" XXX: Esto no aplica, porque el jefe es el único con usuario.
    # TODO: 3. Check si esa Persona ya valido email
    # 4. Check si fue aprobado por el admin, sino mostrar un mensaje o marcarlos con un bool
    user = get_user(username)
    family = LocalImpl().get_person_by_id(user.id_person)
    family.family_group = [
        member.__dict__ for member in family.family_group
    ]  # to pydantic
    return PersonLogged(
        access_token=access_token, token_type="bearer", data=family.__dict__
    )
