from sqlalchemy import Column, Integer, String

from app.config.database import Base

class Category(Base):

    __tablename__ = "category"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)

