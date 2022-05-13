from typing import List
from pydantic import BaseModel


class PersonsReduced(BaseModel):
    id: int
    username: str
    name: str
    surname: str
    id_admin_status: bool
    id_person_status: bool


class Person(BaseModel):
    username: str
    name: str
    surname: str
    id_admin_status: bool
    id_person_status: bool


class PersonUsername(BaseModel):
    username: str


class ListOfPersons(BaseModel):
    persons: List[Person]
