import os

# openssl rand -hex 32
SECRET_KEY = os.getenv("SECRET_KEY", "secret-key")  # FIXME: cambiar esto en producción
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 240  # TODO: hablar con frontend para saber el tiempo ideal

# Database
DATABASE_DEFAULT = os.getenv("DATABASE_ENGINE", "mysql").lower()  # mysql or sqlite
DATABASE_URL = os.getenv("DATABASE_URL")
# e.g. mysql+pymysql://root:root@127.0.0.1:3306/portal_paciente_LR
