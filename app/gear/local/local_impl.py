from datetime import datetime, timedelta

from fastapi import Request, status
from fastapi.responses import Response
from jose import jwt
from sqlalchemy.orm import Session
from pprint import pprint

from app.config.config import SECRET_KEY, ALGORITHM
from app.config.config import WHITE_LIST_PATH
from app.config.database import SessionLocal
from app.models.expiration_black_list import ExpirationBlackList as model_expiration_black_list
from app.models.user import User as model_user
from app.models.permission import Permission as model_permission
from app.models.role_permission import RolePermission as model_role_permission
from app.models.user_role import UserRole as model_user_role
from app.models.message import Message as model_message
from app.models.user_message import UserMessage as model_user_message
from app.schemas.user import User as schema_user
import re


class LocalImpl:

    db: Session = SessionLocal()

    def get_payload_from_bearer_schema(self, bearer_schema: str):
        token = bearer_schema.split("Bearer ")[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload


    async def filter_request_for_authorization(self, request: Request, call_next):

        if request.scope["path"] not in WHITE_LIST_PATH:

            auth_token = request.headers.get("Authorization")

            # Verificación de existencia del token y de que sea válido...
            if auth_token is None or self.is_token_expired(auth_token):
                return Response(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content="Non valid token, expired or not provided.",
                )

            # Verificación de permisos...
            if not self.is_user_authorized(request.scope["path"], request.scope["method"],
                                           self.get_payload_from_bearer_schema(auth_token)):
                return Response(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content="Request not authorized for current user.",
                )

        response = await call_next(request)
        return response

    def get_users(self):
        value = self.db.query(model_user).fetchall()
        return value

    def create_user(self, user: schema_user):
        new_user = model_user()

        new_user.username = user.username
        new_user.password = user.password
        new_user.id_person = user.id_person
        new_user.id_user_status = user.id_user_status

        self.db.add(new_user)
        self.db.commit()
        value = self.db.query(model_user).where(model_user.id == new_user.id).first()
        return value

    def get_user_by_id(self, user_id: int):
        value = self.db.query(model_user).where(model_user.id == user_id).first()
        return value

    def get_user_by_username(self, username: str):
        value = self.db.query(model_user).where(model_user.username == username).first()
        return value

    def delete_user(self, user_id: str):
        old_user = self.db.query(model_user).where(model_user.id == user_id).first()
        self.db.delete(old_user)
        self.db.commit()
        return old_user

    def set_expiration_black_list(self, token: str):
        expiration_black_list = model_expiration_black_list()

        expiration_black_list.register_datetime = datetime.now()
        expiration_black_list.token = token

        self.db.add(expiration_black_list)
        self.db.commit()
        value = (
            self.db.query(model_expiration_black_list)
            .where(model_expiration_black_list.id == expiration_black_list.id)
            .first()
        )

        return value

    def delete_old_tokens(self):

        timestamp = datetime.now() - timedelta(days=1)

        expiration_black_list_elements = self.db.query(model_expiration_black_list).where(model_expiration_black_list.register_datetime < timestamp).all()

        for e in expiration_black_list_elements:
            self.db.delete(e)

        self.db.commit()

    def is_token_expired(self, bearer_schema: str):
        token = bearer_schema.split("Bearer ")[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        expires = datetime.fromtimestamp(payload.get("exp"))
        disabled = False

        if expires < datetime.now():
            self.set_expiration_black_list(token)
            disabled = True

        self.delete_old_tokens()

        return disabled

    def is_user_authorized(self, path: str, method: str, payload: dict):

        username = payload.get("sub")
        enabled = False

        permissions = self.db.query(model_permission)\
            .join(model_role_permission, model_permission.id == model_role_permission.id_permission)\
            .join(model_user_role, model_role_permission.id_role == model_user_role.id_role)\
            .join(model_user, model_user_role.id_user == model_user.id and model_user.username == username)\
            .all()

        value = path
        for p in permissions:
            patterns = [p.url]
            pattern = '(?:% s)' % '|'.join(patterns)
            if re.match(pattern, value) and p.method.upper() == method.upper():
                enabled = True

        return enabled

    def get_messages(self, only_unread: bool, request: Request):

        auth_token = request.headers.get("Authorization")
        payload = self.get_payload_from_bearer_schema(auth_token)
        username = payload.get("sub")

        messages = self.db.query(model_message, model_user_message.read_datetime)\
            .join(model_user_message, model_user_message.id_message == model_message.id)\
            .join(model_user, model_user.id == model_user_message.id_user)\
            .where(model_user_message.read_datetime == None if only_unread else True)\
            .where(model_user.username == username)\
            .all()

        return messages

    def set_messages_read(self, request: Request, message_id: int):

        auth_token = request.headers.get("Authorization")
        payload = self.get_payload_from_bearer_schema(auth_token)
        username = payload.get("sub")

        user_message = self.db.query(model_user_message)\
            .join(model_user, model_user_message.id_user == model_user.id
                  and model_user_message.id_message == message_id
                  and model_user.username == username)\
            .first()

        user_message.read_datetime = datetime.now()

        self.db.commit()

