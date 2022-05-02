import datetime
from pathlib import Path
from typing import Union

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from jose import jwt
from sqlalchemy.orm import Session

from app.config.config import (
    MAIL_FROM,
    MAIL_PORT,
    MAIL_PASSWORD,
    MAIL_SERVER,
    MAIL_USERNAME,
    SECRET_KEY,
    ALGORITHM,
    VALIDATION_MAIL_URL,
)
from app.config.database import SessionLocal
from app.gear.log.main_logger import MainLogger, logging
from app.models.person import Person
from app.models.user import User
from app.schemas.responses import ResponseNOK, ResponseOK
from jose.exceptions import JWTError


conf = ConnectionConfig(
    MAIL_USERNAME=MAIL_USERNAME,
    MAIL_FROM=MAIL_FROM,
    MAIL_PASSWORD=MAIL_PASSWORD,
    MAIL_PORT=MAIL_PORT,
    MAIL_SERVER=MAIL_SERVER,
    MAIL_TLS=True,
    MAIL_SSL=False,
    TEMPLATE_FOLDER=Path("/code/app/templates/"),  # FIXME: fix this
)

db: Session = SessionLocal()

log = MainLogger()
module = logging.getLogger(__name__)

JWT_AUD = "validation-mail"


class ValidationError(Exception):
    """Some Error during the validation mail"""


# TODO: Refactorizar esto, dejar la logica de email acá,
# que el modulo de recover_password use estas cosas
# y que la parte de validación vaya a otro modulo.
# La generación del token debería ir a un utils/
async def send_validation_mail(person_id: str) -> bool:
    existing_person = (
        db.query(Person).where(Person.id == person_id).first()
    )  # type: Person
    if existing_person is None:
        log.log_error_message("Mail Validation - Person, doesn't exist", module)
        return False

    user = db.query(User).where(User.id_person == existing_person.id).first()
    if bool(user.is_mail_validate):
        log.log_error_message("Mail Validation - User already validated", module)
        return False

    validation_url = generate_validation_url(user)
    await _send_email(
        existing_person.email,
        existing_person.name,
        existing_person.surname,
        validation_url,
    )
    log.log_info_message("Email sent successfully.", module)
    return True


def generate_validation_url(user: User) -> str:
    now = datetime.datetime.now()
    claims = {
        "exp": now + datetime.timedelta(hours=24),
        "iss": user.username,
        "iat": now,
        "aud": JWT_AUD,
    }
    token = jwt.encode(claims, SECRET_KEY, algorithm=ALGORITHM)
    url = f"{VALIDATION_MAIL_URL}/{token}/"
    log.log_info_message(f"Created url={url}", module)
    return url


async def _send_email(recipients: str, name: str, surname: str, validation_link: str):
    body = {"name": name, "surname": surname, "validation_link": validation_link}

    message = MessageSchema(
        subject="Validación de cuenta - Portal de Pacientes La Rioja",
        recipients=[recipients],  # List of recipients, as many as you can pass
        template_body=body,
        subtype="html",
    )

    fm = FastMail(conf)
    await fm.send_message(message, template_name="validate-mail.html")


async def validate_email(token: str) -> Union[ResponseNOK, ResponseOK]:
    to_verify = {
        'verify_signature': True,
        'verify_aud': True,
        'verify_exp': True,
        'require_aud': True,
        'require_iat': True,
        'require_exp': True,
        'require_iss': True,
    }
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options=to_verify, audience=JWT_AUD)
    try:
        username = payload["iss"]
        user = db.query(User).where(User.username == username).first()
        if user is None:
            raise ValidationError(f"User doesn't exist")
        # Validate user and save
        if bool(user.is_mail_validate):
            raise ValidationError(f"User already validated")
        user.is_mail_validate = 1
        db.commit()
    except (KeyError, ValidationError) as err:
        log.log_error_message(f"Error: {str(err)}", module)
        return ResponseNOK(message="Something wrong, mail cannot be validated.", code=400)
    except JWTError as err:
        log.log_error_message(f"Something wrong with the token decode: {str(err)}")
        return ResponseNOK(message="Something wrong, mail cannot be validated.", code=400)
    return ResponseOK(message="User validated successfully", code=200)
