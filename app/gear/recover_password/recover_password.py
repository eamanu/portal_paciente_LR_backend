import datetime
from typing import Union

from fastapi_mail import MessageSchema
from jose import jwt
from jose.exceptions import JWTError
from sqlalchemy.orm import Session

from app.config.config import (
    SECRET_KEY,
    ALGORITHM,
    RECOVERY_PASSWORD_URL,
    DEBUG_MAIL_VALIDATION,
)
from app.gear.log.main_logger import MainLogger, logging
from app.gear.mailer.mailer import send_email
from app.models.person import Person
from app.models.user import User
from app.schemas.admin_status_enum import AdminStatusEnum
from app.schemas.responses import ResponseOK, ResponseNOK


log = MainLogger()
module = logging.getLogger(__name__)

JWT_AUD = "recovery-password"

RECOVERY_PASSWORD_TEMPLATE = "recovery-password.html"


class ValidationError(Exception):
    """Some Error during the validation mail"""


def generate_validation_url(user: User) -> str:
    now = datetime.datetime.now()
    claims = {
        "exp": now + datetime.timedelta(hours=4),
        "iss": user.username,
        "iat": now,
        "aud": JWT_AUD,
    }
    token = jwt.encode(claims, SECRET_KEY, algorithm=ALGORITHM)
    url = f"{RECOVERY_PASSWORD_URL}/{token}/"
    log.log_info_message(f"Created url={url}", module)
    return url


async def send_recovery_password_mail(email: str, db: Session) -> bool:
    existing_person = (
        db.query(Person).where(Person.email == email).first()
    )  # type: Person

    if existing_person is None:
        log.log_info_message(f"User with email={email} doesn't exist.", module)
        return False

    if existing_person.id_admin_status != AdminStatusEnum.validated.value:
        log.log_info_message(
            f"User with email={email} was not validated by "
            f"the ADMIN user or was denied",
            module,
        )
        return False

    user = db.query(User).where(User.id_person == existing_person.id).first()
    if not user.is_mail_validate:
        log.log_info_message(
            f"User with email={email} didn't validate email",
            module,
        )
        return False

    if user.is_admin:
        log.log_info_message(
            f"[DANGER] Trying to recover admin user password",
            module,
        )
        return False

    recover_url = generate_validation_url(user)
    recipients = (
        DEBUG_MAIL_VALIDATION if DEBUG_MAIL_VALIDATION else existing_person.email
    )  # TODO: REMOVE THIS BEFORE GO TO PRODUCTION
    await _send_recovery_password_mail(
        recipients, existing_person.name, existing_person.surname, recover_url
    )
    return True


async def _send_recovery_password_mail(
    recipients: str, name: str, surname: str, validation_link: str
):
    body = {"name": name, "surname": surname, "validation_link": validation_link}

    message = MessageSchema(
        subject="Recupero de contraseña - Portal de Pacientes La Rioja",
        recipients=[recipients],  # List of recipients, as many as you can pass
        template_body=body,
        subtype="html",
    )
    await send_email(message, RECOVERY_PASSWORD_TEMPLATE)


async def recover_password(token: str, password: str, db: Session) -> Union[ResponseNOK, ResponseOK]:
    to_verify = {
        "verify_signature": True,
        "verify_aud": True,
        "verify_exp": True,
        "require_aud": True,
        "require_iat": True,
        "require_exp": True,
        "require_iss": True,
    }
    payload = jwt.decode(
        token, SECRET_KEY, algorithms=[ALGORITHM], options=to_verify, audience=JWT_AUD
    )
    try:
        username = payload["iss"]
        user = db.query(User).where(User.username == username).first()
        if user is None:
            raise ValidationError(f"User doesn't exist")
        # Validate user and save
        if not user.is_mail_validate:
            raise ValidationError(f"User didn't validate email")
        user.password = User.encrypt_pwd(password)
        db.commit()
    except (KeyError, ValidationError) as err:
        log.log_error_message(f"Error: {str(err)}", module)
        return ResponseNOK(
            message="Something wrong, password cannot be change.", code=400
        )
    except JWTError as err:
        log.log_error_message(f"Something wrong with the token decode: {str(err)}")
        return ResponseNOK(message="Something wrong, password cannot be change.", code=400)
    except Exception as e:
        db.rollback()
    return ResponseOK(message="User password change", code=200)
