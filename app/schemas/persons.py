from typing import List, Optional
from pydantic import BaseModel


class PersonsReduced(BaseModel):
    id: int
    username: str
    name: str
    surname: str
    id_admin_status: int
    id_person_status: int
    id_usual_institution: Optional[int]


class Person(BaseModel):
    username: str
    name: str
    surname: str
    id_admin_status: int
    id_person_status: int


class PersonUsername(BaseModel):
    username: str


class ListOfPersons(BaseModel):
    persons: List[Person]
