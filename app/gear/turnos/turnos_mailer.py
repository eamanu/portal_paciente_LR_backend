from fastapi_mail import MessageSchema
from sqlalchemy.orm import Session

from app.config.config import (
    DEBUG_MAIL_VALIDATION,
)
from app.config.database import SessionLocal
from app.gear.log.main_logger import MainLogger, logging
from app.gear.mailer.mailer import send_email
from app.models.person import Person


db: Session = SessionLocal()

log = MainLogger()
module = logging.getLogger(__name__)


async def send_turno_mail(person_id: str, subject: str, body: str) -> bool:
    existing_person = (
        db.query(Person).where(Person.id == person_id).first()
    )  # type: Person

    # TODO: REMOVE THIS BEFORE GO TO PRODUCTION
    recipients = (DEBUG_MAIL_VALIDATION if DEBUG_MAIL_VALIDATION else existing_person.email)
    message = MessageSchema(
        subject=subject,
        recipients=[recipients],  # List of recipients, as many as you can pass
        body=body,
        # subtype="html",
    )

    # TODO: Almacenar person_id + subject (y un status? o fecha?) en la base de datos,
    #  después vemos que se puede hacer

    await send_email(message)
    log.log_info_message("Email sent successfully.", module)
    return True
