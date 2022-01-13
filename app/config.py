import os

# openssl rand -hex 32
SECRET_KEY = os.getenv("SECRET_KEY", "secret-key")  # FIXME: cambiar esto en producción
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10  # TODO: hablar con frontend para saber el tiempo ideal
