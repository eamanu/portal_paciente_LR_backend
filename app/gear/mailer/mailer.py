from pathlib import Path
from typing import Optional

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

from app.config.config import (
    MAIL_FROM,
    MAIL_PORT,
    MAIL_PASSWORD,
    MAIL_SERVER,
    MAIL_USERNAME,
    TEMPLATE_FOLDER_VALIDATION_MAIL,
)
from app.gear.log.main_logger import MainLogger, logging


log = MainLogger()
module = logging.getLogger(__name__)


async def send_email(message: MessageSchema, template_name: Optional[str] = None):
    conf = ConnectionConfig(
        MAIL_USERNAME=MAIL_USERNAME,
        MAIL_FROM=MAIL_FROM,
        MAIL_PASSWORD=MAIL_PASSWORD,
        MAIL_PORT=MAIL_PORT,
        MAIL_SERVER=MAIL_SERVER,
        MAIL_TLS=True,
        MAIL_SSL=False,
        TEMPLATE_FOLDER=Path(TEMPLATE_FOLDER_VALIDATION_MAIL),
    )

    fm = FastMail(conf)
    log.log_info_message(f"Sending mail to {message.recipients}...", module)
    await fm.send_message(message, template_name=template_name)
