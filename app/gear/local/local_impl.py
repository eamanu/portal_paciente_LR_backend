from datetime import datetime

from fastapi import Request, status
from fastapi.responses import JSONResponse
from jose import jwt
from sqlalchemy.orm import Session

from app.config.config import SECRET_KEY, ALGORITHM
from app.config.database import SessionLocal
from app.models.expiration_black_list import ExpirationBlackList as model_expiration_black_list
from app.models.user import User as model_user
from app.schemas.user import User as schema_user


class Local_Impl:
    db: Session = SessionLocal()

    async def filter_request_for_authorization(self, request: Request, call_next):
        # TODO: should be in config.py ¿?
        if request.scope["path"] != "/portalpaciente/api/v1/login":

            # Verificación de existencia del token...
            if not request.scope["headers"][0][0] == b'authorization':
                return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content="")

            # Verificación del token válido...
            if self.is_token_expired(request.scope["headers"][0][1]):
                return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content="")

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

        expiration_black_list.register_datetime = datetime.utcnow()
        expiration_black_list.token = token

        self.db.add(expiration_black_list)
        self.db.commit()
        value = self.db.query(model_expiration_black_list).where(
            model_expiration_black_list.id == expiration_black_list.id).first()

        return value

    @staticmethod
    def is_token_expired(token: str):
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        expires = datetime.fromtimestamp(payload.get("exp"))

        if expires < datetime.utcnow():
            Local_Impl().set_expiration_black_list(token)
            return True
        return False
