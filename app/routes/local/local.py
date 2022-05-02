from datetime import datetime
from pathlib import Path
from typing import List

from fastapi import Depends, HTTPException, status, File, UploadFile
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.config.config import SECRET_KEY, ALGORITHM
from app.gear.local.local_impl import LocalImpl
from app.gear.log.main_logger import MainLogger, logging
from app.gear.mailer.mailer import validate_email
from app.gear.recover_password.recover_password import send_recovery_password_mail, recover_password
from app.main import get_db
from app.routes import auth
from app.routes.common import router_local
from app.schemas.category import Category
from app.schemas.message import Message
from app.schemas.message import ReadMessage
from app.schemas.person import (
    Person as schema_person,
    CreatePerson as schema_create_person,
)
from app.schemas.person import PersonLogged
from app.schemas.person_status import PersonStatus
from app.schemas.person_user import PersonUser as schema_person_user
from app.schemas.responses import HTTPError
from app.schemas.responses import ResponseOK, ResponseNOK
from app.schemas.role import Role
from app.schemas.token import Token


oauth_schema = OAuth2PasswordBearer(tokenUrl="/login")

log = MainLogger()
module = logging.getLogger(__name__)


@router_local.get("/version")
async def version():
    with open(Path("./app/VERSION"), "r") as f:
        version = f.read().strip()
    return {"version": version}


@router_local.post(
    "/login-admin",
    response_model=Token,
    responses={401: {"model": HTTPError}},
    tags=["Login & Logout"],
)
async def login_for_access_token(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    return auth.login_for_access_token(db, form_data)


@router_local.post(
    "/login",
    response_model=PersonLogged,
    responses={401: {"model": HTTPError}},
    tags=["Login & Logout"],
)
async def login_person(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    return auth.login_person(db, form_data)


@router_local.post("/logout", tags=["Login & Logout"])
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


# @router_local.post("/createuser", response_model=ResponseOK, responses={417: {"model": ResponseNOK}}, tags=["User and person"])
# async def create_user(user: schema_user):
#    return LocalImpl().create_user(user)


@router_local.post(
    "/createmessage",
    response_model=ResponseOK,
    responses={417: {"model": ResponseNOK}},
    tags=["Message"],
)
async def create_message(header: str, body: str, is_formatted: bool):
    return LocalImpl().create_message(header, body, is_formatted)


@router_local.put(
    "/updatemessage",
    response_model=ResponseOK,
    responses={417: {"model": ResponseNOK}},
    tags=["Message"],
)
async def update_message(message: Message):
    return LocalImpl().update_message(message)


@router_local.put(
    "/deletemessage",
    response_model=ResponseOK,
    responses={417: {"model": ResponseNOK}},
    tags=["Message"],
)
async def delete_message(message_id: int):
    return LocalImpl().delete_message(message_id)


@router_local.post(
    "/sendmessage",
    response_model=ResponseOK,
    responses={417: {"model": ResponseNOK}},
    tags=["Message"],
)
async def send_message(message_id: int, category_id: int, is_for_all_categories: bool):
    return LocalImpl().send_message(message_id, category_id, is_for_all_categories)


@router_local.get(
    "/get-messages-by-person",
    response_model=List[ReadMessage],
    responses={417: {"model": ResponseNOK}},
    tags=["Message"],
)
async def get_messages_by_person(person_id: int, only_unread: bool):
    return LocalImpl().get_messages(person_id, only_unread)


@router_local.get(
    "/getmessage",
    response_model=Message,
    responses={417: {"model": ResponseNOK}},
    tags=["Message"],
)
async def get_message(message_id: int):
    return LocalImpl().get_message(message_id)


@router_local.get(
    "/get-all-messages",
    response_model=List[Message],
    responses={417: {"model": ResponseNOK}},
    tags=["Message"],
)
async def get_all_messages():
    return LocalImpl().get_all_messages()


@router_local.post(
    "/setmessageread",
    response_model=ResponseOK,
    responses={417: {"model": ResponseNOK}},
    tags=["Message"],
)
async def set_message_read(person_id: int, message_id: int):
    return LocalImpl().set_message_read(person_id, message_id)


@router_local.post(
    "/createperson",
    response_model=ResponseOK,
    responses={417: {"model": ResponseNOK}},
    tags=["User and person"],
)
async def create_person(person: schema_create_person):
    return LocalImpl().create_person(person)


@router_local.put(
    "/updateperson",
    response_model=ResponseOK,
    responses={417: {"model": ResponseNOK}},
    tags=["User and person"],
)
async def update_person(person: schema_person):
    return LocalImpl().update_person(person)


@router_local.put(
    "/deleteperson",
    response_model=ResponseOK,
    responses={417: {"model": ResponseNOK}},
    tags=["User and person"],
)
async def delete_person(person_id: int):
    return LocalImpl().delete_person(person_id)


@router_local.get(
    "/getpersonbyid", response_model=schema_person, tags=["User and person"]
)
async def get_person_by_id(person_id: int):
    return LocalImpl().get_person_by_id(person_id)


@router_local.get(
    "/getpersonbyidentificationnumber",
    response_model=schema_person,
    tags=["User and person"],
)
async def get_person_by_identification_number(person_identification_number: str):
    return LocalImpl().get_person_by_identification_number(person_identification_number)


@router_local.put(
    "/setadminstatustoperson",
    response_model=ResponseOK,
    responses={417: {"model": ResponseNOK}},
    tags=["Admin"],
)
async def set_admin_status_to_person(person_id: int, admin_status_id: int):
    return LocalImpl().set_admin_status_to_person(person_id, admin_status_id)


@router_local.post(
    "/createpersonanduser",
    response_model=ResponseOK,
    responses={417: {"model": ResponseNOK}},
    tags=["User and person"],
)
async def create_person_and_user(person_user: schema_person_user):
    return LocalImpl().create_person_and_user(person_user)


@router_local.get(
    "/getpersonstatus",
    response_model=List[PersonStatus],
    responses={417: {"model": ResponseNOK}},
    tags=["User and person"],
)
async def get_person_status():
    return LocalImpl().get_person_status()


@router_local.get(
    "/getroles",
    response_model=List[Role],
    responses={417: {"model": ResponseNOK}},
    tags=["User and person"],
)
async def get_roles():
    return LocalImpl().get_roles()


@router_local.get(
    "/getcategories",
    response_model=List[Category],
    responses={417: {"model": ResponseNOK}},
    tags=["User and person"],
)
async def get_categories():
    return LocalImpl().get_categories()


@router_local.post(
    "/uploadidentificationimages",
    response_model=ResponseOK,
    responses={417: {"model": ResponseNOK}},
    tags=["User and person"],
)
async def upload_identification_images(
    person_id: str, file1: UploadFile = File(...), file2: UploadFile = File(...)
):
    return await LocalImpl().upload_identification_images(person_id, file1, file2)


@router_local.get("/validate-email/{token}/", tags=["User and person"])
async def val_email(token: str):
    return await validate_email(token)


@router_local.get("/recover-password", tags=["User and person"])
async def send_email_to_recover_password(email: str):
    result = await send_recovery_password_mail(email)
    if not result:
        log.log_info_message("Mail don't sent to recover password", module)

    return ResponseOK(message="A email was sent you if the email exists in the system.", code=200)


@router_local.get("/change-password", tags=["User and person"])
async def change_password_password(token: str, password: str):
    return await recover_password(token, password)
