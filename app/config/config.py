import os

# openssl rand -hex 32
SECRET_KEY = os.getenv("SECRET_KEY", "i-hate-w1nd0w$$")  # TODO: Remove this
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 240

# Database
DATABASE_DEFAULT = os.getenv("DATABASE_ENGINE", "mysql").lower()  # mysql or sqlite
DATABASE_URL = os.getenv("DATABASE_URL")
# e.g. mysql+pymysql://root:root@127.0.0.1:3306/portal_paciente_LR

# Whitelisted Paths
WHITE_LIST_PATH = ("/portalpaciente/api/v1/login", "/docs", "/openapi.json", "/favicon.ico", "/")

