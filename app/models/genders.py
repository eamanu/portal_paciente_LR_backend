from sqlalchemy import Column, Integer, String

from app.config.database import Base

class Gender(Base):

    __tablename__ = "gender"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)