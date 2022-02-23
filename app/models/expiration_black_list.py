from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.config.database import Base

class ExpirationBlackList(Base):

    __tablename__ = "expiration_black_list"

    id = Column(Integer, primary_key=True, autoincrement=True)
    register_datetime = Column(DateTime, nullable=False)
    token = Column(String(500), nullable=False)

    def __init__(self, register_datetime: datetime, token: str):
        self.register_datetime = register_datetime
        self.token = token
