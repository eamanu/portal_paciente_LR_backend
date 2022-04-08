import os

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
    "/portalpaciente/api/v1/login",
    "/portalpaciente/api/v1/logout",
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