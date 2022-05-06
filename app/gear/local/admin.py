from app.config.database import SessionLocal
from sqlalchemy.orm import Session
from app.schemas.persons import PersonsReduced, Person, PersonUsername
from typing import List
from app.schemas.returned_object import ReturnMessage

db: Session = SessionLocal()


# TODO: dev purpose. remove this
class Persons():
    username: str
    name: str
    accepted: bool
    is_deleted: bool

    def __init__(self, username, name, accepted, is_deleted):
        self.username = username
        self.name = name
        self.accepted = accepted
        self.is_deleted = is_deleted


def list_of_persons():
    """
    Return list of persons, only name surname and if is accepted or
    not in the system.
    """
    persons: List[Persons] = db.query(Persons).where(Persons.is_deleted == False).all()

    return [
        PersonsReduced(
            username=person.username,
            name=person.name,
            accepted=person.accepted
        ) for person in persons
    ]


def list_of_persons_to_accept():
    """
    Return list of persons, only name and surname of persons that
    need to be accepted.
    """

    persons: List[Persons] = db.query(Persons).where(
        Persons.is_deleted == False and Persons.accepted == False).all()

    return [
        PersonsReduced(
            username=person.username,
            name=person.name,
            accepted=person.accepted
        ) for person in persons
    ]


def accept_a_person(person_username: PersonUsername):
    """Accept a new person in the system

    :param person_username: username of the system
    :return: 204 if was procesed or 202 if failed
    """
    try:
        db.query(Persons).filter(Persons.username==person_username.username).update({"accepted": True})
    except Exception:
        return {"message": "Person cannot be updated", "code": 202}
    return {"message": "Person accepted successfully", "code": 204}


def not_accept_a_person(person_username: PersonUsername):
    """Not Accept a new person in the system

    :param person_username: username of the system
    :return: 204 if was procesed or 202 if failed
    """
    try:
        db.query(Persons).filter(Persons.username==person_username.username).update({"accepted": False})
        db.commit()
    except Exception:
        return {"message": "Person cannot be updated", "code": 202}
    return {"message": "Person not accepted successfully", "code": 204}


def remove_a_person(person_username: PersonUsername):
    """Remove a user from the system.

    *Note*: this method don't remove a person from database, it
    will mark as removed and that person will not be shown.

    :param person_username: user to remove
    :return: 204 if was removed, 202 otherwise.
    """
    try:
        db.query(Persons).filter(Persons.username==person_username.username).update({"is_deleted": True})
        db.commit()
    except Exception:
        return {"message": "Person cannot be updated", "code": 202}
    return {"message": "Person not accepted successfully", "code": 204}


def create_a_new_person(new_person: Person):
    """Create a new person from admin

    :param new_person: Pydantic object
    :return:
    """
    person = Persons(**new_person.dict())
    db.add(person)
    db.commit()

    return ReturnMessage(message="New person created successfully", code=204)
