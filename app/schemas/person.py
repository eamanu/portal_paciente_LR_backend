from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel, validator
from pydantic.typing import List


class Person(BaseModel):
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
    identification_front_image: Optional[str]
    identification_back_image: Optional[str]
    identification_front_image_file_type: Optional[str]
    identification_back_image_file_type: Optional[str]
    id_person_status: Optional[int]
    family_group: Optional[list]

    @validator("birthdate", pre=True)
    def parse_birthdate(cls, value):
        # XXX: Tenemos un problema entre schemas y modelos que no son compatibles
        # por lo que esto es necesario. No eliminar.
        if isinstance(value, str):
            return datetime.strptime(value, "%d/%m/%Y")
        return datetime.combine(value, datetime.min.time())

    class Config:
        orm_mode = True


class CreatePerson(BaseModel):
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

    @validator("birthdate", pre=True)
    def parse_birthdate(cls, value):
        return datetime.strptime(value, "%d/%m/%Y")


class CreatePersonResponse(BaseModel):
    id: Optional[int]
    surname: Optional[str]
    name: Optional[str]
    identification_number: Optional[str]
    birthdate: Optional[date]
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

    class Config:
        orm_mode = True


class Person2(BaseModel):
    id: Optional[int]
    surname: Optional[str]
    name: Optional[str]
    identification_number: Optional[str]
    birthdate: Optional[date]
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


class PersonFamily(BaseModel):
    id: Optional[int]
    surname: Optional[str]
    name: Optional[str]
    identification_number: Optional[str]
    birthdate: Optional[date]
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
    family_group: List[Person2]


class PersonLogged(BaseModel):
    id_person: int
    access_token: str
    token_type: str
    data: PersonFamily
