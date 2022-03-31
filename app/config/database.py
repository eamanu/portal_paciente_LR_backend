#region Imports

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config.config import DATABASE_DEFAULT, DATABASE_URL

# endregion

SQLITE = 'sqlite'
MYSQL = 'mysql'

if DATABASE_DEFAULT == SQLITE:
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)

conn = engine.connect()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
from app.models import (  # noqa
    category,
    expiration_black_list,
    message,
    permission,
    role,
    role_permission,
    user,
    user_category,
    user_front_end,
    user_message,
    user_role,
)

meta = MetaData()

# endregion
