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

Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
meta = MetaData()
conn = engine.connect()

# endregion
