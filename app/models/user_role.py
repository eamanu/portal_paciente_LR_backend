from sqlalchemy import Column, Integer, String

from app.config.database import Base

class UserRole(Base):

    __tablename__ = "user_role"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_role = Column(Integer, nullable=False)
    id_user = Column(Integer, nullable=False)

