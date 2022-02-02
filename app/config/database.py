#region Imports

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# endregion

# region SQLite

# SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
SQLALCHEMY_DATABASE_URL = "sqlite:///./app/portal_paciente.db"
engine01 = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
#SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine01)

Base = declarative_base()

# endregion

# region MySql

MYSQL_DATABASE_URL = "mysql+pymysql://root:root@127.0.0.1:3306/portal_paciente_LR"
engine02 = create_engine(MYSQL_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine02)

meta = MetaData()

conn = engine02.connect()

# endregion