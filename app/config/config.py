import os

# region Base API names

LR_BASE_API = "/portalpaciente/api/v1"

# endregion

# region openssl rand -hex 32

SECRET_KEY = os.getenv("SECRET_KEY", "i-hate-w1nd0w$$")  # TODO: Remove this
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 240

# endregion

# region Database

DATABASE_DEFAULT = os.getenv("DATABASE_ENGINE", "mysql").lower()  # mysql or sqlite
DATABASE_URL = os.getenv("DATABASE_URL")
# e.g. mysql+pymysql://root:root@127.0.0.1:3306/portal_paciente_LR

# endregion

# region Whitelisted Paths

WHITE_LIST_PATH = (
    LR_BASE_API + "/login",
    LR_BASE_API + "/logout",
    LR_BASE_API + "/static",
    "/docs",
    "/openapi.json",
    "/favicon.ico",
    "/",
)

# endregion

# region Logging

LOG_FORMAT = '[%(asctime)s][%(levelname)s][%(name)s][%(message)s]'
LOG_PATH = './app.log'

# endregion

# region Operational mode

DEBUG_ENABLED = False
AUTHORIZATION_ENABLED = False

# endregion

# region File configurations

LOCAL_FILE_UPLOAD_DIRECTORY = os.getenv("TMP_FILES_UPLOAD")
LOCAL_FILE_DOWNLOAD_DIRECTORY = os.getenv("TMP_FILES_DOWNLOAD")

# endregion

# region mail configuration

# TODO: Esto va a dejar de funcionar le 30 de mayo
MAIL_USERNAME = os.getenv("MAIL_USERNAME", "")
MAIL_FROM = os.getenv("MAIL_FROM", "no@mail.com")  # ConnectionConfig object need it as a valid mail format
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "")
MAIL_PORT = os.getenv("MAIL_PORT", 123)
MAIL_SERVER = os.getenv("MAIL_SERVER", "")

# endregion

# region validation-mail

SERVER_IP = os.getenv("SERVER_IP", "http://127.0.0.1:8000")
VALIDATION_ENDPOINT = os.getenv("VALIDATION_ENDPOINT", LR_BASE_API + "/validate-email")
VALIDATION_MAIL_URL = f"{SERVER_IP}{VALIDATION_ENDPOINT}"

# endregion

# region recover-password

RECOVERY_ENDPOINT = os.getenv("RECOVERY_ENDPOINT", LR_BASE_API + "/recovery-password")
RECOVERY_PASSWORD_URL = f"{SERVER_IP}{RECOVERY_ENDPOINT}"

# endregion
