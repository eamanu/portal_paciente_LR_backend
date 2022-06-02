from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from app.gear.hsi.config import HSI_DATABASE_URL

engine = create_engine(HSI_DATABASE_URL, poolclass=NullPool)

SessionLocalHSI = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

meta = MetaData()
