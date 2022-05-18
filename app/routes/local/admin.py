from app.gear.local.admin import (
    remove_a_person,
    not_accept_a_person,
    accept_a_person,
    list_of_persons_to_accept,
    list_of_persons_accepted,
    list_of_persons_in_general
)
from app.routes.common import router_admin
from app.schemas.persons import Person, PersonUsername, PersonsReduced
from app.schemas.returned_object import ReturnMessage
from typing import List


@router_admin.delete("/person", name="Remove a Person",
                     response_model=ReturnMessage, description="Remove a Person from the system")
async def delete_person(person_username: PersonUsername):
    return remove_a_person(person_username)


@router_admin.put("/notaccept", name="Deny access to a Person",
                  response_model=ReturnMessage, description="Denied access to a person")
async def not_accept_person(person_username: PersonUsername):
    return not_accept_a_person(person_username)


@router_admin.put("/id_admin_status", name="Accept a Person",
                  response_model=ReturnMessage, description="Accept a Person in the system")
async def accept_person(person_username: PersonUsername):
    return accept_a_person(person_username)


@router_admin.get("/persons_accepted", name="List of id_admin_status Person", response_model=List[PersonsReduced], description="List of Persons id_admin_status in the system")
async def persons_accepted():
    return list_of_persons_accepted()

@router_admin.get("/persons_to_be_accepted", name="List of id_admin_status Person", response_model=List[PersonsReduced], description="List of Persons to be id_admin_status in the system")
async def persons_accepted():
    return list_of_persons_to_accept()

@router_admin.get("/persons", name= "List of persons", response_model=List[PersonsReduced], description="List of all Persons in the system")
async def persons():
    return list_of_persons_in_general()

