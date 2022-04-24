from sqlalchemy import Column, Integer, DateTime

from app.config.database import Base


class PersonMessage(Base):
    __tablename__ = "person_message"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_person = Column(Integer, nullable=False)
    id_message = Column(Integer, nullable=False)
    read_datetime = Column(DateTime, nullable=False)
