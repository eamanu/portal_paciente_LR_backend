from sqlalchemy import Column, Integer, String

from app.config.database import Base

class UserCategory(Base):

    __tablename__ = "user_category"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_user = Column(Integer, nullable=False)
    id_category = Column(Integer, nullable=False)

