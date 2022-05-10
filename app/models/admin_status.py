from sqlalchemy import Column, Integer, String

from app.config.database import Base

class AdminStatus(Base):

    __tablename__ = "admin_status"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)

    def __init__(self, name: str):
        self.name = name
