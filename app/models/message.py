from sqlalchemy import Column, Integer, String, DateTime, Boolean

from app.config.database import Base


class Message(Base):
    __tablename__ = "message"

    id = Column(Integer, primary_key=True, autoincrement=True)
    register_datetime = Column(DateTime, nullable=False)
    header = Column(String(500), nullable=False)
    body = Column(String(4000), nullable=False)
    is_formatted = Column(Boolean, nullable=False)

