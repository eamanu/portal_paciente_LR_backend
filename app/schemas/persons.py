from typing import List
from pydantic import BaseModel


class PersonsReduced(BaseModel):
    username: str
    name: str
    surname: str
    accepted: bool


class Person(BaseModel):
    username: str
    name: str
    surname: str
    accepted: bool


class PersonUsername(BaseModel):
    username: str


class ListOfPersons(BaseModel):
    persons: List[Person]
