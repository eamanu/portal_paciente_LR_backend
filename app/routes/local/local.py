from datetime import datetime

from fastapi import Depends, HTTPException, Request, status, File, UploadFile
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.config.config import SECRET_KEY, ALGORITHM
from app.gear.local.local_impl import LocalImpl
from app.main import get_db
from app.routes import auth
from app.routes.common import router_local
from app.schemas.token import Token
from app.schemas.user import User as schema_user
from app.schemas.person import Person as schema_person
from app.schemas.person_user import PersonUser as schema_person_user


oauth_schema = OAuth2PasswordBearer(tokenUrl="/login")


@router_local.post("/login", response_model=Token)
async def login_for_access_token(db: Session = Depends(get_db),
                                 form_data: OAuth2PasswordRequestForm = Depends()):
    return auth.login_for_access_token(db, form_data)


@router_local.post("/logout")
async def logout(token: str = Depends(oauth_schema)):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        expires = datetime.fromtimestamp(payload.get("exp"))
        if expires is None:
            raise credentials_exception
        LocalImpl().set_expiration_black_list(token)
        return {"msg": "good bye"}

    except JWTError:
        raise credentials_exception


@router_local.post("/createuser")
async def create_user(user: schema_user):
    return LocalImpl().create_user(user)


@router_local.get("/getmessages")
async def get_messages(only_unread: bool, request: Request):
    return LocalImpl().get_messages(only_unread, request)


@router_local.post("/setmessagesread")
async def set_messages_read(request: Request, message_id: int):
    return LocalImpl().set_messages_read(request, message_id)


@router_local.post("/createperson")
async def create_person(person: schema_person):
    return LocalImpl().create_person(person)


@router_local.put("/updateperson")
async def update_person(person: schema_person):
    return LocalImpl().update_person(person)


@router_local.put("/deleteperson")
async def delete_person(person_id: int):
    return LocalImpl().delete_person(person_id)


@router_local.get("/getpersonbyid")
async def get_person_by_id(person_id: int):
    return LocalImpl().get_person_by_id(person_id)


@router_local.get("/getpersonbyidentificationnumber")
async def get_person_by_identification_number(person_identification_number: str):
    return LocalImpl().get_person_by_identification_number(person_identification_number)


@router_local.put("/setadminstatustoperson")
async def set_admin_status_to_person(person_id: int, admin_status_id: int):
    return LocalImpl().set_admin_status_to_person(person_id, admin_status_id)


@router_local.put("/setadminstatustoperson")
async def set_admin_status_to_person(person_id: int, admin_status_id: int):
    return LocalImpl().set_admin_status_to_person(person_id, admin_status_id)


@router_local.post("/createpersonanduser")
async def create_person_and_user(person_user: schema_person_user):
    return LocalImpl().create_person_and_user(person_user)

@router_local.post("/uploadidentificationimages")
async def upload_identification_images(person_id: str, file: UploadFile = File(...), file2: UploadFile = File(...)):
    return LocalImpl().upload_identification_images(person_id, file, file2)
