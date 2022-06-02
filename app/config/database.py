#region Imports

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config.config import DATABASE_DEFAULT, DATABASE_URL

# endregion

#region DB settings

SQLITE = 'sqlite'
MYSQL = 'mysql'

if DATABASE_DEFAULT == SQLITE:
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL, pool_size=20, max_overflow=0)

conn = engine.connect()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

meta = MetaData()

# endregion
