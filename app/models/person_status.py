from sqlalchemy import Column, Integer, String

from app.config.database import Base

class PersonStatus(Base):

    __tablename__ = "person_status"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)

    def __init__(self, name: str):
        self.name = name
