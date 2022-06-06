import base64
import uuid
from datetime import datetime, timedelta
from typing import Optional, Union

from fastapi import Request, status, File, UploadFile
from fastapi.responses import Response
from jose.exceptions import JWTError
from sqlalchemy.exc import PendingRollbackError
from sqlalchemy.orm import Session

from app.config.config import (
    WHITE_LIST_PATH,
    AUTHORIZATION_ENABLED,
    DEBUG_ENABLED,
    LOCAL_FILE_UPLOAD_DIRECTORY,
    LOCAL_FILE_DOWNLOAD_DIRECTORY,
    VALIDATE_EMAIL_PATH,
)
from app.gear.local.bearer_token import BearerToken
from app.gear.log.main_logger import MainLogger, logging
from app.gear.validation_mail.validation_mail import send_validation_mail
from app.models.admin_status import AdminStatus as model_admin_status
from app.models.category import Category as model_category
from app.models.expiration_black_list import (
    ExpirationBlackList as model_expiration_black_list,
)
from app.models.genders import Gender as model_gender
from app.models.message import Message as model_message
from app.models.permission import Permission
from app.models.person import Person as model_person
from app.models.person_message import PersonMessage as model_person_message
from app.models.person_status import PersonStatus as model_person_status
from app.models.role import Role as model_role
from app.models.user import User as model_user
from app.schemas.category_enum import CategoryEnum
from app.schemas.message import Message, ReadMessage
from app.schemas.person import (
    Person as schema_person,
    CreatePerson as schema_create_person,
)
from app.schemas.person_user import PersonUser as schema_person_user
from app.schemas.responses import ResponseNOK, ResponseOK
from app.schemas.user import User as schema_user


class LocalImpl:

    log = MainLogger()
    module = logging.getLogger(__name__)

    def __init__(self, db: Session):
        self.db = db

    async def filter_request_for_authorization(self, request: Request, call_next):

        if DEBUG_ENABLED:
            print(vars(request))

        # TODO: Check if this is necessary:
        #  Look a way to respond to preflighs from frontend.

        if request.method == "OPTIONS":
            return Response(
                status_code=status.HTTP_204_NO_CONTENT,
                headers={
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "POST, GET, OPTIONS, DELETE, PUT",
                    "Access-Control-Max-Age": "86400",
                    "Access-Control-Allow-Headers": "*",
                    "Content-type": "*"
                }
            )

        if AUTHORIZATION_ENABLED and (request.scope["path"] not in WHITE_LIST_PATH and
                                      VALIDATE_EMAIL_PATH not in request.scope["path"]):

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
                request.scope["path"],
                request.scope["method"],
                bearer_token.payload,
                request,
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
            return ResponseNOK(message="Users cannot be retrieved.", code=417)
        return value

    def create_user(self, user: schema_user) -> Union[ResponseOK, ResponseNOK]:
        try:
            new_user = model_user(**user.dict())
            self.db.add(new_user)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            self.log.log_error_message(e, self.module)
            return ResponseNOK(message="User not created.", code=417)
        return ResponseOK(message="User created successfully.", code=201)

    def get_user_by_id(self, user_id: int):
        try:
            value = self.db.query(model_user).where(model_user.id == user_id).first()
        except Exception as e:
            self.log.log_error_message(e, self.module)
            return ResponseNOK(message="User cannot be retrieved.", code=202)
        return value

    def get_user_by_username(self, username: str):
        try:
            value = (
                self.db.query(model_user).where(model_user.username == username).first()
            )
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
            self.db.rollback()
            self.log.log_error_message(e, self.module)
            return ResponseNOK(message="User cannot be deleted.", code=417)
        return ResponseOK(message="User deleted successfully.", code=201)

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
            self.db.rollback()
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
            self.db.rollback()
            self.log.log_error_message(e, self.module)
            return True

    def is_token_expired(self, bearer_token: BearerToken) -> bool:
        try:
            payload = bearer_token.payload
        except JWTError as err:
            self.log.log_error_message(
                str(err) + " [" + str(bearer_token) + "]", self.module
            )
            return True

        if payload is None or self.is_token_black_listed(bearer_token.token):
            self.log.log_error_message(
                "Nonexistent payload or token included in black list.", self.module
            )
            return True

        is_expired = bearer_token.is_expired
        if is_expired:
            self.set_expiration_black_list(bearer_token.token)
        self.delete_old_tokens()
        return is_expired

    def is_user_authorized(
        self, path: str, method: str, payload: Optional[dict], request=None
    ) -> bool:
        try:
            if payload is None:
                return False
            username = payload.get("sub")

            # check if the user is in DB
            user = self.db.query(model_user).where(model_user.username == username).first()
            if user is None:
                return False

            # return Permission.user_is_authorized(username, path, method)
            return Permission.user_is_authorized2(username, request)
        except Exception as e:
            MainLogger().log_error_message(e, logging.getLogger(__name__))
            return False

    def create_message(self, header: str, body: str, is_formatted: bool):
        try:

            new_message = model_message()

            new_message.header = header
            new_message.body = body
            new_message.is_formatted = is_formatted

            self.db.add(new_message)
            self.db.commit()

        except Exception as e:
            self.db.rollback()
            self.log.log_error_message(e, self.module)
            return ResponseNOK(message="Message not created.", code=417)

        return ResponseOK(
            value=str(new_message.id), message="Message created successfully.", code=201
        )

    def update_message(self, message: Message):
        try:
            existing_message = (
                self.db.query(model_message)
                .where(model_message.id == message.id)
                .first()
            )

            existing_message.header = message.header
            existing_message.body = message.body
            existing_message.is_formatted = message.is_formatted

            self.db.commit()

        except Exception as e:
            self.db.rollback()
            self.log.log_error_message(e, self.module)
            return ResponseNOK(message="Message not updated.", code=417)

        return ResponseOK(message="Message updated successfully.", code=201)

    def delete_message(self, message_id: int):
        try:
            message = (
                self.db.query(model_message)
                .where(model_message.id == message_id)
                .first()
            )
            if message is None:
                return ResponseOK(message="Nonexistent message.", code=200)

            self.db.delete(message)
            self.db.commit()

        except Exception as e:
            self.db.rollback()
            self.log.log_error_message(e, self.module)
            return ResponseNOK(message=f"Error: {str(e)}", code=417)
        return ResponseOK(message="Message deleted successfully.", code=200)

    def send_message(
        self, message_id: int, category_id: int, is_for_all_categories: bool
    ):
        try:
            create_relation = False
            receipt_found = False

            existing_persons = self.db.query(model_person).all()
            for p in existing_persons:
                if is_for_all_categories:
                    receipt_found = True
                    create_relation = True
                else:
                    if category_id == CategoryEnum.diabetic.value and p.is_diabetic:
                        receipt_found = True
                        create_relation = True
                    else:
                        if (
                            category_id == CategoryEnum.hypertensive.value
                            and p.is_hypertensive
                        ):
                            receipt_found = True
                            create_relation = True
                        else:
                            if (
                                category_id
                                == CategoryEnum.chronic_respiratory_disease.value
                                and p.is_chronic_respiratory_disease
                            ):
                                receipt_found = True
                                create_relation = True
                            else:
                                if (
                                    category_id
                                    == CategoryEnum.chronic_kidney_disease.value
                                    and p.is_chronic_kidney_disease
                                ):
                                    receipt_found = True
                                    create_relation = True
                if create_relation:

                    new_person_message = model_person_message()
                    new_person_message.id_person = p.id
                    new_person_message.id_message = message_id

                    self.db.add(new_person_message)
                    self.db.commit()

                create_relation = False

            if receipt_found:

                message = (
                    self.db.query(model_message)
                    .where(model_message.id == message_id)
                    .first()
                )
                if message is None:
                    return ResponseOK(message="Nonexistent message.", code=200)

                message.sent_datetime = datetime.now()
                self.db.commit()

        except Exception as e:
            self.db.rollback()
            self.log.log_error_message(e, self.module)
            return ResponseNOK(message="Message relation not created.", code=417)
        return ResponseOK(message="Message relation created successfully.", code=201)

    def get_messages(self, person_id: int, only_unread: bool):
        try:
            messages = (
                self.db.query(model_message, model_person_message.read_datetime)
                .join(
                    model_person_message,
                    model_person_message.id_message == model_message.id,
                )
                .join(model_person, model_person.id == model_person_message.id_person)
                .where(model_person.id == person_id)
            )

            result = []
            for message, read_time in messages:
                if only_unread and read_time is not None:
                    continue
                message_schema = Message.from_orm(message)
                read_message = ReadMessage(
                    message=message_schema, read_datetime=read_time
                )
                result.append(read_message)
        except Exception as e:
            self.log.log_error_message(e, self.module)
            return ResponseNOK(message=f"Error: {str(e)}", code=417)

        return result

    def get_all_messages(self):
        try:
            messages = self.db.query(model_message).all()
        except Exception as e:
            self.log.log_error_message(e, self.module)
            return ResponseNOK(message=f"Error: {str(e)}", code=417)

        return messages

    def get_message(self, message_id: int):
        try:
            message = (
                self.db.query(model_message)
                .where(model_message.id == message_id)
                .first()
            )

        except Exception as e:
            self.log.log_error_message(e, self.module)
            return ResponseNOK(message=f"Error: {str(e)}", code=417)

        return message

    def set_message_read(self, person_id: int, message_id: int):
        try:

            person_message = (
                self.db.query(model_person_message)
                .where(model_person_message.id_person == person_id)
                .where(model_person_message.id_message == message_id)
                .first()
            )

            person_message.read_datetime = datetime.now()

            self.db.commit()

            return ResponseOK(message="Message set read successfully.", code=201)
        except Exception as e:
            self.db.rollback()
            self.log.log_error_message(e, self.module)
            return ResponseNOK(message=f"Error: {str(e)}", code=417)

    def create_person(self, person: schema_create_person):
        buff_person = (
            self.db.query(model_person)
            .where(model_person.identification_number == person.identification_number)
            .first()
        )
        if buff_person is not None:
            return ResponseNOK(value="", message="Person already exists.", code=417)
        try:
            new_person = model_person(**person.dict())

            new_person.is_deleted = None

            self.db.add(new_person)
            self.db.commit()

            return ResponseOK(
                value=str(new_person.id),
                message="Person created successfully.",
                code=201,
            )

        except Exception as e:
            self.db.rollback()
            self.log.log_error_message(e, self.module)
            return ResponseNOK(value="", message="Person not created.", code=417)

    def update_person(self, person: schema_person) -> Union[ResponseOK, ResponseNOK]:
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
            existing_person.is_chronic_respiratory_disease = (
                updated_person.is_chronic_respiratory_disease
            )
            existing_person.is_chronic_kidney_disease = (
                updated_person.is_chronic_kidney_disease
            )
            existing_person.identification_number_master = (
                updated_person.identification_number_master
            )
            existing_person.id_identification_type = (
                updated_person.id_identification_type
            )
            existing_person.id_identification_type_master = (
                updated_person.id_identification_type_master
            )
            existing_person.is_deleted = updated_person.is_deleted
            existing_person.id_patient = updated_person.id_patient
            existing_person.id_admin_status = updated_person.id_admin_status
            existing_person.phone_number = updated_person.phone_number
            existing_person.department = updated_person.department
            existing_person.locality = updated_person.locality
            existing_person.email = updated_person.email
            existing_person.id_person_status = updated_person.id_person_status

            existing_person.is_deleted = None

            self.db.commit()
            return ResponseOK(
                value=str(existing_person.id),
                message="Person updated successfully.",
                code=201,
            )

        except Exception as e:
            self.db.rollback()
            self.log.log_error_message(e, self.module)
            return ResponseNOK(message="Person cannot be updated.", code=417)

    def delete_person(self, person_id: int):
        try:
            old_person = (
                self.db.query(model_person).where(model_person.id == person_id).first()
            )
            old_person.is_deleted = None
            self.db.commit()
            old_person.is_deleted = True
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            self.log.log_error_message(e, self.module)
            return ResponseNOK(message="Person cannot be deleted.", code=417)
        return ResponseOK(message="Person deleted successfully.", code=201)

    def get_person_by_id(self, person_id: int):
        return self.get_person(person_id, None, True)

    def get_person_by_identification_number(self, person_identification_number: str):
        return self.get_person(0, person_identification_number, False)

    def get_person(
        self,
        person_id: int,
        person_identification_number: Optional[str],
        is_by_id: bool,
    ):

        existing_person = None

        try:

            if is_by_id:
                existing_person = (
                    self.db.query(model_person)
                    .where(model_person.id == person_id)
                    .first()
                )
            else:
                existing_person = (
                    self.db.query(model_person)
                    .where(
                        model_person.identification_number
                        == person_identification_number
                    )
                    .first()
                )

            if existing_person is None:
                return ResponseNOK(message="Nonexistent Person.", code=417)

        except Exception as e:
            self.log.log_error_message(e, self.module)
            return ResponseNOK(
                message=f"Person cannot be retrieved. Error: {str(e)}", code=417
            )

        # s_person = schema_person.from_orm(existing_person)
        s_person = self.get_schema_person_from_model_person(existing_person)

        s_person.family_group = self.get_family_group_by_identification_number_master(
            s_person.identification_number
        )

        return s_person

    def get_family_group_by_identification_number_master(
        self, identification_number_master: str
    ):

        s_family_group = []

        family_group = (
            self.db.query(model_person)
            .where(
                model_person.identification_number_master
                == identification_number_master
            )
            .all()
        )

        filter_family = [
            person
            for person in family_group
            if person.identification_number != identification_number_master
        ]

        if filter_family != "[]":
            for eperson in filter_family:
                # s_family_group.append(schema_person.from_orm(eperson))
                s_family_group.append(self.get_schema_person_from_model_person(eperson))

        return s_family_group

    # TODO: Tal vez se puede borrar este método porque no se usa.
    # pero dejarlo, por las dudas rompa los cambios que hice en el
    # schema de Personas.
    # Lo tuve que volver a usar, porque este método permite retornar
    # sólo los campos que uno quiere. Ejemplo: las imágenes del DNI.
    def get_schema_person_from_model_person(self, m_person: model_person):
        s_person = schema_person()
        s_person.id = m_person.id
        s_person.name = m_person.name
        s_person.surname = m_person.surname
        s_person.birthdate = m_person.birthdate
        # s_person.identification_front_image = m_person.identification_front_image
        s_person.identification_front_image_file_type = (
            m_person.identification_front_image_file_type
        )
        # s_person.identification_back_image = m_person.identification_back_image
        s_person.identification_back_image_file_type = (
            m_person.identification_back_image_file_type
        )
        s_person.id_person_status = m_person.id_person_status
        s_person.id_admin_status = m_person.id_admin_status
        s_person.id_gender = m_person.id_gender
        s_person.id_patient = m_person.id_patient
        s_person.id_usual_institution = m_person.id_usual_institution
        s_person.locality = m_person.locality
        s_person.id_locality = m_person.id_locality
        s_person.department = m_person.department
        s_person.id_department = m_person.id_department
        s_person.phone_number = m_person.phone_number
        s_person.identification_number = m_person.identification_number
        s_person.id_identification_type = m_person.id_identification_type
        s_person.identification_number_master = m_person.identification_number_master
        s_person.id_identification_type_master = m_person.id_identification_type_master
        s_person.is_diabetic = m_person.is_diabetic
        s_person.is_hypertensive = m_person.is_hypertensive
        s_person.is_chronic_kidney_disease = m_person.is_chronic_kidney_disease
        s_person.is_chronic_respiratory_disease = (
            m_person.is_chronic_respiratory_disease
        )
        s_person.address_street = m_person.address_street
        s_person.address_number = m_person.address_number
        s_person.email = m_person.email
        s_person.is_deleted = m_person.is_deleted

        return s_person

    def set_admin_status_to_person(self, person_id: int, admin_status_id: int):
        try:
            existing_person = (
                self.db.query(model_person).where(model_person.id == person_id).first()
            )
            existing_person.id_admin_status = admin_status_id
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            self.log.log_error_message(e, self.module)
            return ResponseNOK(
                message=f"Person cannot be updated. Error: {str(e)}", code=417
            )
        return ResponseOK(message="Admin status set successfully.", code=201)

    def create_person_and_user(self, person_user: schema_person_user):
        person = (
            self.db.query(model_person)
            .where(
                model_person.identification_number == person_user.identification_number
                or model_person.email == person_user.email
            )
            .first()
        )
        if person is not None:
            return ResponseNOK(message="Person already exists.", code=417)

        user = (
            self.db.query(model_user)
            .where(model_user.username == person_user.username)
            .first()
        )
        if user is not None:
            return ResponseNOK(message="Username already exists.", code=417)
        try:
            new_person = model_person(
                None,
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
                person_user.email,
                person_user.id_person_status,
            )

            new_person.is_deleted = None

            self.db.add(new_person)
            self.db.commit()

            value = (
                self.db.query(model_person)
                .where(model_person.id == new_person.id)
                .first()
            )

            new_user = model_user(
                person_user.username,
                person_user.password,
                value.id,
                person_user.id_user_status,
            )

            self.db.add(new_user)
            self.db.commit()

            return ResponseOK(
                value=str(new_person.id),
                message="Person and user created successfully.",
                code=201,
            )

        except Exception as e:
            self.db.rollback()
            return ResponseNOK(
                message=f"Person and user cannot be created. Error: {str(e)}", code=417
            )

    def get_admin_status(self):
        try:
            result = []
            collection = self.db.query(model_admin_status).all()

            for u in collection:
                result.append({"id": u.id, "name": u.name})

            return result

        except Exception as e:
            self.log.log_error_message(e, self.module)
            return ResponseNOK(message=f"Error: {str(e)}", code=417)

    def get_person_status(self):
        try:
            result = []
            collection = self.db.query(model_person_status).all()

            for u in collection:
                result.append({"id": u.id, "name": u.name})

            return result

        except Exception as e:
            self.log.log_error_message(e, self.module)
            return ResponseNOK(message=f"Error: {str(e)}", code=417)

    def get_roles(self):
        try:
            result = []
            collection = self.db.query(model_role).all()

            for u in collection:
                result.append({"id": u.id, "name": u.name})

            return result
        except Exception as e:
            self.log.log_error_message(e, self.module)
            return ResponseNOK(message=f"Error: {str(e)}", code=417)

    def get_categories(self):
        try:
            result = []
            categories = self.db.query(model_category).all()

            for u in categories:
                result.append({"id": u.id, "name": u.name})

            return result
        except Exception as e:
            self.log.log_error_message(e, self.module)
            return ResponseNOK(message=f"Error: {str(e)}", code=417)

    def get_genders(self):
        try:
            result = []
            collection = self.db.query(model_gender).all()

            for u in collection:
                result.append({"id": u.id, "name": u.name})

            return result
        except Exception as e:
            self.log.log_error_message(e, self.module)
            return ResponseNOK(message=f"Error: {str(e)}", code=417)

    async def upload_identification_images(
        self,
        person_id: str,
        file1: UploadFile = File(...),
        file2: UploadFile = File(...),
    ):
        existing_person = (
            self.db.query(model_person).where(model_person.id == person_id).first()
        )

        if existing_person is None:
            return ResponseNOK(
                message=f"Nonexistent person_id: {str(person_id)}", code=417
            )

        try:
            # File 1 ------------------------------------------------------------------------------------
            destination_file_path = (
                LOCAL_FILE_UPLOAD_DIRECTORY + file1.filename
            )  # location to store file
            file_a = open(destination_file_path, "wb+")
            file_a.write(await file1.read())
            file_a.close()
            with open(destination_file_path, "rb") as bin_file:
                b64_string_file1 = base64.b64encode(bin_file.read())

            # File 2 ------------------------------------------------------------------------------------
            destination_file_path = (
                LOCAL_FILE_UPLOAD_DIRECTORY + file2.filename
            )  # location to store file
            file_b = open(destination_file_path, "wb+")
            file_b.write(await file2.read())
            file_b.close()
            with open(destination_file_path, "rb") as bin_file:
                b64_string_file2 = base64.b64encode(bin_file.read())

            # Saving process -----------------------------------------------------------------------------
            existing_person.identification_front_image = b64_string_file1
            existing_person.identification_back_image = b64_string_file2
            existing_person.identification_front_image_file_type = file1.content_type
            existing_person.identification_back_image_file_type = file2.content_type
            self.db.commit()

            # validating email
            await send_validation_mail(person_id, self.db)

        except Exception as e:
            self.db.rollback()
            self.log.log_error_message(e, self.module)
            return ResponseNOK(message=f"Error: {str(e)}", code=417)
        return ResponseOK(message="Files uploaded successfully.", code=201)

    def download_identification_image(self, person_id: str, is_front: bool):
        try:

            file_name = None
            existing_person = (
                self.db.query(model_person).where(model_person.id == person_id).first()
            )

            if existing_person is None:
                return ResponseNOK(
                    message=f"Nonexistent person_id: {str(person_id)}", code=417
                )

            destination_file_path = LOCAL_FILE_DOWNLOAD_DIRECTORY

            if is_front:
                if existing_person.identification_front_image_file_type is not None:
                    file_name = (
                        str(uuid.uuid4())
                        + "."
                        + existing_person.identification_front_image_file_type[
                            (
                                existing_person.identification_front_image_file_type.rfind(
                                    "/"
                                )
                                + 1
                            ) :
                        ]
                    )
                    base64_img_bytes = (
                        existing_person.identification_front_image.encode("utf-8")
                    )
            else:
                if existing_person.identification_back_image_file_type is not None:
                    file_name = (
                        str(uuid.uuid4())
                        + "."
                        + existing_person.identification_back_image_file_type[
                            (
                                existing_person.identification_back_image_file_type.rfind(
                                    "/"
                                )
                                + 1
                            ) :
                        ]
                    )
                    base64_img_bytes = existing_person.identification_back_image.encode(
                        "utf-8"
                    )

            if file_name is not None:
                with open(destination_file_path + file_name, "wb") as file_to_save:
                    decoded_image_data = base64.decodebytes(base64_img_bytes)
                    file_to_save.write(decoded_image_data)
                file_to_save.close()
            else:
                return ResponseNOK(message="Nonexistent image.", code=417)

        except Exception as e:
            self.log.log_error_message(e, self.module)
            return ResponseNOK(message=f"Error: {str(e)}", code=417)
        return ResponseOK(
            value="/static/" + file_name,
            message="File downloaded successfully.",
            code=201,
        )
