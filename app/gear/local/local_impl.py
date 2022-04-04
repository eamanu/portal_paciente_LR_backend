from datetime import datetime, timedelta
from typing import Optional

from fastapi import Request, status
from fastapi.responses import Response
from jose.exceptions import JWTError
from sqlalchemy.exc import PendingRollbackError
from sqlalchemy.orm import Session

from app.config.config import WHITE_LIST_PATH
from app.config.database import SessionLocal
from app.gear.local.bearer_token import BearerToken
from app.models.expiration_black_list import (
    ExpirationBlackList as model_expiration_black_list,
)
from app.models.message import Message as model_message
from app.models.permission import Permission
from app.models.user import User as model_user
from app.models.user_message import UserMessage as model_user_message
from app.models.person import Person as model_person
from app.schemas.user import User as schema_user
from app.schemas.person import Person as schema_person

from app.gear.log.main_logger import MainLogger, logging


class LocalImpl:

    db: Session = SessionLocal()

    log = MainLogger()
    module = logging.getLogger(__name__)

    async def filter_request_for_authorization(self, request: Request, call_next):

        print(vars(request))

        if request.method == "OPTIONS":
            return Response(
                status_code=status.HTTP_204_NO_CONTENT,
                # should be added to database ?
                headers={
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "POST, GET, OPTIONS, DELETE",
                    "Access-Control-Max-Age": "86400",
                    "Access-Control-Allow-Headers": "authorization",
                }
            )

        if request.scope["path"] not in WHITE_LIST_PATH:

            auth_token = request.headers.get("Authorization")
            bearer_token = BearerToken(auth_token)

            # Verificación de existencia del token y de que sea válido...
            if auth_token is None or self.is_token_expired(bearer_token):

                if bearer_token.payload is not None:
                    self.log.log_error_message(
                        "Non valid token, expired or not provided for "
                        + bearer_token.payload.get("sub"),
                        self.module,
                    )
                else:
                    self.log.log_error_message(
                        "Non valid token, expired or not provided.", self.module
                    )

                return Response(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content="Non valid token, expired or not provided.",
                )
            # Verificación de permisos...
            if not self.is_user_authorized(
                request.scope["path"], request.scope["method"], bearer_token.payload
            ):
                self.log.log_error_message(
                    "Request not authorized for user "
                    + bearer_token.payload.get("sub"),
                    self.module,
                )

                return Response(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content="Request not authorized for current user.",
                )

        response = await call_next(request)
        return response

    def get_users(self):
        try:
            value = self.db.query(model_user).fetchall()
        except Exception as e:
            self.log.log_error_message(e, self.module)
        return value

    def create_user(self, user: schema_user):
        try:
            new_user = model_user(**user.dict())
            self.db.add(new_user)
            self.db.commit()
            value = (
                self.db.query(model_user).where(model_user.id == new_user.id).first()
            )
        except Exception as e:
            self.log.log_error_message(e, self.module)
        return value

    def get_user_by_id(self, user_id: int):
        try:
            value = self.db.query(model_user).where(model_user.id == user_id).first()
        except Exception as e:
            self.log.log_error_message(e, self.module)
        return value

    def get_user_by_username(self, username: str):
        try:
            value = self.db.query(model_user).where(model_user.username == username).first()
            return value
        except PendingRollbackError as e:
            self.log.log_error_message(str(e) + " [" + username + "]", self.module)
            self.db.rollback()
            return None
        except Exception as e:
            self.log.log_error_message(e, self.module)
            return None

    def delete_user(self, user_id: str):
        try:
            old_user = self.db.query(model_user).where(model_user.id == user_id).first()
            self.db.delete(old_user)
            self.db.commit()
        except Exception as e:
            self.log.log_error_message(e, self.module)
        return old_user

    def is_token_black_listed(self, token: str) -> bool:
        try:
            where_cond = model_expiration_black_list.token == token
            return bool(
                self.db.query(model_expiration_black_list).where(where_cond).first()
            )
        except Exception as e:
            self.log.log_error_message(e, self.module)
        return False

    def set_expiration_black_list(self, token: str) -> None:
        try:
            expiration_black_list = model_expiration_black_list(
                register_datetime=datetime.now(), token=token
            )
            self.db.add(expiration_black_list)
            self.db.commit()
        except Exception as e:
            self.log.log_error_message(e, self.module)

    def delete_old_tokens(self):
        try:
            timestamp = datetime.now() - timedelta(days=1)

            expiration_black_list_elements = (
                self.db.query(model_expiration_black_list)
                .where(model_expiration_black_list.register_datetime < timestamp)
                .all()
            )

            for e in expiration_black_list_elements:
                self.db.delete(e)

            self.db.commit()
        except Exception as e:
            self.log.log_error_message(e, self.module)
            return True

    def is_token_expired(self, bearer_token: BearerToken) -> bool:
        try:
            payload = bearer_token.payload
        except JWTError as err:
            # cambiar a logger
            # print(err)
            self.log.log_error_message(
                str(err) + " [" + str(bearer_token) + "]", self.module
            )
            return True

        if payload is None or self.is_token_black_listed(bearer_token.token):
            self.log.log_error_message(
                "Non existent payload or token is in black list.", self.module
            )
            return True

        is_expired = bearer_token.is_expired
        if is_expired:
            self.set_expiration_black_list(bearer_token.token)
        self.delete_old_tokens()
        return is_expired

    @staticmethod
    def is_user_authorized(path: str, method: str, payload: Optional[dict]) -> bool:
        try:
            if payload is None:
                return False
            username = payload.get("sub")
            return Permission.user_is_authorized(username, path, method)
        except Exception as e:
            MainLogger().log_error_message(e, logging.getLogger(__name__))
            return False

    def get_messages(self, only_unread: bool, request: Request):
        try:
            bearer_token = BearerToken(request.headers.get("Authorization"))
            username = bearer_token.payload.get("sub")

            messages = (
                self.db.query(model_message, model_user_message.read_datetime)
                .join(
                    model_user_message,
                    model_user_message.id_message == model_message.id,
                )
                .join(model_user, model_user.id == model_user_message.id_user)
                .where(
                    model_user_message.read_datetime is None if only_unread else True
                )
                .where(model_user.username == username)
                .all()
            )

            return messages
        except Exception as e:
            self.log.log_error_message(e, self.module)

    def set_messages_read(self, request: Request, message_id: int):
        try:
            bearer_token = BearerToken(request.headers.get("Authorization"))
            username = bearer_token.payload.get("sub")

            user_message = (
                self.db.query(model_user_message)
                .join(
                    model_user,
                    model_user_message.id_user == model_user.id
                    and model_user_message.id_message == message_id
                    and model_user.username == username,
                )
                .first()
            )

            user_message.read_datetime = datetime.now()

            self.db.commit()
        except Exception as e:
            self.log.log_error_message(e, self.module)
            return True

    def create_person(self, person: schema_person):
        try:
            new_person = model_person(**person.dict())
            self.db.add(new_person)
            self.db.commit()
            value = (
                self.db.query(model_person).where(model_person.id == new_person.id).first()
            )
        except Exception as e:
            self.log.log_error_message(e, self.module)
        return value
