from fastapi_mail import MessageSchema
from sqlalchemy.orm import Session

from app.config.config import (
    MAIL_USERNAME,
)
from app.gear.log.main_logger import MainLogger, logging
from app.gear.mailer.mailer import send_email
from app.main import get_db
from app.models.person import Person


db: Session = next(get_db())

log = MainLogger()
module = logging.getLogger(__name__)


async def send_turno_mail(person_id: str, subject: str, body: str) -> bool:
    existing_person = (
        db.query(Person).where(Person.id == person_id).first()
    )  # type: Person

    message = MessageSchema(
        subject=subject,
        recipients=[MAIL_USERNAME],
        body=body,
        # subtype="html",
    )

    # TODO: Almacenar person_id + subject (y un status? o fecha?) en la base de datos,
    #  después vemos que se puede hacer

    await send_email(message)
    log.log_info_message("Email sent successfully.", module)
    return True
