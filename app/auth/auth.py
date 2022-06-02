from datetime import timedelta, datetime
from typing import Optional

from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.config.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from app.main import get_db
from app.models.user import User
from app.schemas.token_data import TokenData
from app.gear.local.local_impl import LocalImpl

from app.gear.log.main_logger import MainLogger, logging

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

log = MainLogger()
module = logging.getLogger(__name__)


# TODO: get_user no debería estar en auth.py, debería estar
#  en algún lado más general.
def get_user(username: str) -> Optional[User]:
    # For some issue we need some attemps before failed
    # we need to made a research to understand why get_user_by_username
    # fail with a Exception in ASGI application
    log.log_info_message("getting user", module)
    db = next(get_db())


    # for attemp in range(10):
    #     log.log_info_message(f"getting user, attempt: {attemp}", module)
    #    user = LocalImpl(db).get_user_by_username(username=username)
    #    if user is not None:
    #        return user
    # return None
    user = LocalImpl(db).get_user_by_username(username=username)
    return user


def authenticate_user(db: Session, username: str, password: str) -> bool:
    user = get_user(username)
    if user is None:
        return False
    return user.check_password(password) and not user.admin


def authenticate_user_and_is_admin(db: Session, username: str, password: str) -> bool:
    user = get_user(username)
    if user is None:
        return False
    return user.check_password(password) and user.admin


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):

    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


async def get_current_user(db: Session, token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            log.log_error_message("Non specified user.", module)
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError as e:
        log.log_error_message(str(e) + " [" + str(token_data.username) + "]", module)
        raise credentials_exception
    user = get_user(db, username=token_data.username)
    if user is None:
        log.log_error_message("Non existent user " + str(token_data.username), module)
        raise credentials_exception
    return user
