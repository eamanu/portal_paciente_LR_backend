from sqlalchemy import Column, Integer, String

from app.config.database import Base

class RolePermission(Base):

    __tablename__ = "role_permission"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_permission = Column(Integer, nullable=False)
    id_role = Column(Integer, nullable=False)

