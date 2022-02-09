from sqlalchemy import Column, Integer, String

from app.config.database import Base

class Permission(Base):

    __tablename__ = "permission"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    url = Column(String(1000), nullable=False)
    method = Column(String(10), nullable=False)

