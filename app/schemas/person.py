from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class Person(BaseModel):
    # id: Optional[int]
    surname: Optional[str]
    name: Optional[str]
    identification_number: Optional[str]
    birthdate: Optional[datetime]
    id_gender: Optional[int]
    id_department: Optional[int]
    id_locality: Optional[int]
    address_street: Optional[str]
    address_number: Optional[str]
    id_usual_institution: Optional[int]
    is_diabetic: Optional[bool]
    is_hypertensive: Optional[bool]
    is_chronic_respiratory_disease: Optional[bool]
    is_chronic_kidney_disease: Optional[bool]
    identification_number_master: Optional[str]

