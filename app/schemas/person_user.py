from typing import Optional
from pydantic import BaseModel, validator
from datetime import datetime


class PersonUser(BaseModel):
    id: Optional[int]
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
    id_identification_type: Optional[int]
    id_identification_type_master: Optional[int]
    is_deleted: Optional[bool]
    id_patient: Optional[int]
    id_admin_status: Optional[int]
    phone_number: Optional[str]
    department: Optional[str]
    locality: Optional[str]
    email: Optional[str]
    id_person_status: Optional[int]
    #####################
    # User
    #####################
    username: Optional[str]
    password: Optional[str]
    id_person: Optional[int]
    id_user_status: Optional[int]

    @validator("birthdate", pre=True)
    def parse_birthdate(cls, value):
        return datetime.strptime(
            value,
            "%d/%m/%Y"
        )

