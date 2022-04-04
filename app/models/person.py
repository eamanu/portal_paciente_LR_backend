import bcrypt
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime

from app.config.database import Base


class Person(Base):

    __tablename__ = "person"

    id = Column(Integer, primary_key=True, autoincrement=True)
    surname = Column(String(100), nullable=False)
    name = Column(String(100), nullable=False)
    identification_number = Column(String(100), nullable=False)
    birthdate = Column(DateTime, nullable=False)
    id_gender = Column(Integer, nullable=False)
    id_department = Column(Integer, nullable=False)
    id_locality = Column(Integer, nullable=True)
    address_street = Column(String(250), nullable=False)
    address_number = Column(String(100), nullable=False)
    id_usual_institution = Column(Integer, nullable=False)
    is_diabetic = Column(Boolean, nullable=False)
    is_hypertensive = Column(Boolean, nullable=False)
    is_chronic_respiratory_disease = Column(Boolean, nullable=False)
    is_chronic_kidney_disease = Column(Boolean, nullable=False)
    identification_number_master = Column(String(100), nullable=False)


    def __init__(
        self, surname: str, name: str, identification_number: str, birthdate: datetime, id_gender: int,
            id_department: int, id_locality: int, address_street: str, address_number: str, id_usual_institution: int,
            is_diabetic: bool, is_hypertensive: bool, is_chronic_respiratory_disease: bool,
            is_chronic_kidney_disease: bool, identification_number_master: str):
        self.surname = surname
        self.name = name
        self.identification_number = identification_number
        self.birthdate = birthdate
        self.id_gender = id_gender
        self.id_department = id_department
        self.id_locality = id_locality
        self.address_street = address_street
        self.address_number = address_number
        self.id_usual_institution = id_usual_institution
        self.is_diabetic = is_diabetic
        self.is_hypertensive = is_hypertensive
        self.is_chronic_respiratory_disease = is_chronic_respiratory_disease
        self.is_chronic_kidney_disease = is_chronic_kidney_disease
        self.identification_number_master = identification_number_master
