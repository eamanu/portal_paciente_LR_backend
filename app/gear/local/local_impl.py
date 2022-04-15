from datetime import datetime, timedelta
from typing import Optional

from fastapi import Request, status, File, UploadFile
from fastapi.responses import Response
from jose.exceptions import JWTError
from sqlalchemy.exc import PendingRollbackError
from sqlalchemy.orm import Session
import aiofiles
import base64

from app.config.config import WHITE_LIST_PATH, AUTHORIZATION_ENABLED, DEBUG_ENABLED, LOCAL_FILE_UPLOAD_DIRECTORY
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
from app.schemas.person_user import PersonUser as schema_person_user

from app.gear.log.main_logger import MainLogger, logging


class LocalImpl:

    db: Session = SessionLocal()

    log = MainLogger()
    module = logging.getLogger(__name__)

    async def filter_request_for_authorization(self, request: Request, call_next):

        if DEBUG_ENABLED:
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
                    "Content-type": "application/json"
                }
            )

        if AUTHORIZATION_ENABLED and (request.scope["path"] not in WHITE_LIST_PATH):

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
            return {"message": "Error, person not created", "code": 202}
        return {"message": "Person Create successfully", "code": 201}

    def update_person(self, person: schema_person):

        try:
            updated_person = model_person(**person.dict())

            existing_person = (
                self.db.query(model_person)
                    .where(model_person.id == updated_person.id)
                    .first()
            )

            existing_person.surname = updated_person.surname
            existing_person.name = updated_person.name
            existing_person.identification_number = updated_person.identification_number
            existing_person.birthdate = updated_person.birthdate
            existing_person.id_gender = updated_person.id_gender
            existing_person.id_department = updated_person.id_department
            existing_person.id_locality = updated_person.id_locality
            existing_person.address_street = updated_person.address_street
            existing_person.address_number = updated_person.address_number
            existing_person.id_usual_institution = updated_person.id_usual_institution
            existing_person.is_diabetic = updated_person.is_diabetic
            existing_person.is_hypertensive = updated_person.is_hypertensive
            existing_person.is_chronic_respiratory_disease = updated_person.is_chronic_respiratory_disease
            existing_person.is_chronic_kidney_disease = updated_person.is_chronic_kidney_disease
            existing_person.identification_number_master = updated_person.identification_number_master
            existing_person.id_identification_type = updated_person.id_identification_type
            existing_person.id_identification_type_master = updated_person.id_identification_type_master
            existing_person.is_deleted = updated_person.is_deleted
            existing_person.id_patient = updated_person.id_patient
            existing_person.id_admin_status = updated_person.id_admin_status
            existing_person.phone_number = updated_person.phone_number
            existing_person.department = updated_person.department
            existing_person.locality = updated_person.locality
            existing_person.email = updated_person.email

            self.db.commit()
            value = (
                self.db.query(model_person).where(model_person.id == existing_person.id).first()
            )
        except Exception as e:
            self.log.log_error_message(e, self.module)
        return value

    def delete_person(self, person_id: int):
        try:
            old_person = self.db.query(model_person).where(model_person.id == person_id).first()
            old_person.is_deleted = None
            self.db.commit()
            old_person.is_deleted = True
            self.db.commit()
        except Exception as e:
            self.log.log_error_message(e, self.module)
        return old_person

    def get_person_by_id(self, person_id: int):

        return self.get_person(person_id, None, True)

    def get_person_by_identification_number(self, person_identification_number: str):

        return self.get_person(0, person_identification_number, False)

    def get_person(self, person_id: int, person_identification_number: str, is_by_id: bool):

        try:

            if is_by_id:
                existing_person = self.db.query(model_person).where(model_person.id == person_id).first()
            else:
                existing_person = self.db.query(model_person).where(
                    model_person.identification_number == person_identification_number).first()

            family_group = self.db.query(model_person).where(
                model_person.identification_number_master == existing_person.identification_number).all()

            if family_group != "[]":
                existing_person.family_group = family_group

        except Exception as e:
            self.log.log_error_message(e, self.module)

        return existing_person

    def set_admin_status_to_person(self, person_id: int, admin_status_id: int):
        try:
            existing_person = self.db.query(model_person).where(model_person.id == person_id).first()
            existing_person.id_admin_status = admin_status_id
            self.db.commit()
        except Exception as e:
            self.log.log_error_message(e, self.module)
        return existing_person


    def create_person_and_user(self, person_user: schema_person_user):

        try:

            new_person = model_person(None,
            person_user.surname,
            person_user.name,
            person_user.identification_number,
            person_user.birthdate,
            person_user.id_gender,
            person_user.id_department,
            person_user.id_locality,
            person_user.address_street,
            person_user.address_number,
            person_user.id_usual_institution,
            person_user.is_diabetic,
            person_user.is_hypertensive,
            person_user.is_chronic_respiratory_disease,
            person_user.is_chronic_kidney_disease,
            person_user.identification_number_master,
            person_user.id_identification_type,
            person_user.id_identification_type_master,
            person_user.is_deleted,
            person_user.id_patient,
            person_user.id_admin_status,
            person_user.phone_number,
            person_user.department,
            person_user.locality,
            person_user.email)

            self.db.add(new_person)
            self.db.commit()

            value = (
                self.db.query(model_person).where(model_person.id == new_person.id).first()
            )

            new_user = model_user(person_user.username,
            person_user.password,
            value.id,
            person_user.id_user_status)

            self.db.add(new_user)
            self.db.commit()
        except Exception as e:
            return {"message": "Error, person not created", "code": 202}
        return {"message": "Person Create successfully", "code": 201}


    async def upload_identification_images(self, person_id: str, file: UploadFile = File(...),
                                           file2: UploadFile = File(...)):

        b64_string_file1 = ""
        b64_string_file2 = ""

        print("ESTOY ACÁ...")

        try:

            # File 1 ------------------------------------------------------------------------------------
            destination_file_path = LOCAL_FILE_UPLOAD_DIRECTORY + file.filename  # location to store file

            file_a = open(destination_file_path, "wb+")

            file_a.write(await file.read())

            file_a.close()

            with open(destination_file_path, "rb") as bin_file:
                b64_string_file1 = base64.b64encode(bin_file.read())

            # File 2 ------------------------------------------------------------------------------------
            destination_file_path = LOCAL_FILE_UPLOAD_DIRECTORY + file2.filename  # location to store file

            file_b = open(destination_file_path, "wb+")

            file_b.write(await file2.read())

            file_b.close()

            with open(destination_file_path, "rb") as bin_file:
                b64_string_file2 = base64.b64encode(bin_file.read())

            print("#######################################################")
            print(person_id)
            print(len(b64_string_file1))
            print(len(b64_string_file2))
            print("#######################################################")

            # Saving process -----------------------------------------------------------------------------
            existing_person = (
                self.db.query(model_person)
                    .where(model_person.id == person_id)
                    .first()
            )

            existing_person.identification_front_image = b64_string_file1
            existing_person.identification_back_image = b64_string_file2

            self.db.commit()

        except Exception as e:
            self.log.log_error_message(e, self.module)
            print(e)

        print("ESTOY ACÁ FINALIZANDO...")
        return {"Result": "OK"}
