from app.config.database import SessionLocal
from sqlalchemy.orm import Session
from app.schemas.persons import PersonsReduced, Person, PersonUsername
from app.models.person import Person as model_person
from app.models.user import User as model_user
from app.schemas.returned_object import ReturnMessage
from app.schemas.admin_status_enum import AdminStatusEnum

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


def list_of_persons(only_accepted: bool):
    """
    Return list of persons, only name surname and if is accepted or
    not in the system.
    """

    if only_accepted is None:
        cond = True
    else:
        if only_accepted:
            cond = model_person.id_admin_status == AdminStatusEnum.validated.value
        else:
            cond = (model_person.id_admin_status == AdminStatusEnum.validation_pending.value
                    or model_person.id_admin_status == AdminStatusEnum.validation_rejected.value)

    p_list = db.query(model_person,
                      model_person.id,
                      model_person.surname,
                      model_person.name,
                      model_person.is_deleted,
                      model_person.id_admin_status,
                      model_user.username)\
        .join(model_user, model_user.id_person == model_person.id)\
        .where(model_person.is_deleted is None or model_person.is_deleted == False) \
        .where(cond) \
        .all()

    persons_to_return = []

    for p in p_list:
        persons_to_return.append(PersonsReduced(id=p.id,
                                                username=p.username,
                                                name=p.name,
                                                surname=p.surname,
                                                accepted=(True if p.id_admin_status == AdminStatusEnum.validated.value else False)))


    return persons_to_return


def list_of_persons_accepted():
    return list_of_persons(True)

def list_of_persons_to_accept():
    """
    Return list of persons, only name and surname of persons that
    need to be accepted.
    """
    return list_of_persons(False)

def list_of_persons_in_general():
    """
    Return list of persons, without considering status.
    """
    return list_of_persons(None)

def accept_a_person(person_username: PersonUsername):
    return change_person_status_by_admin(person_username, AdminStatusEnum.validated.value)


def not_accept_a_person(person_username: PersonUsername):
    return change_person_status_by_admin(person_username, AdminStatusEnum.validation_rejected.value)


def change_person_status_by_admin(person_username: PersonUsername, admin_status_id: int):
    try:
        existing_user = db.query(model_user).where(model_user.username == person_username.username).first()

        if existing_user is not None:
            existing_person = db.query(model_person).where(model_person.id == existing_user.id_person).first()

            if existing_person is not None:
                existing_person.id_admin_status = admin_status_id
                db.commit()
            else:
                return ReturnMessage(message="Nonexistent person.", code=417)
        else:
            return ReturnMessage(message="Nonexistent user.", code=417)

    except Exception:
        return ReturnMessage(message="Person cannot be updated.", code=417)

    return ReturnMessage(message="Person updated successfully.", code=201)



def remove_a_person(person_username: PersonUsername):
    try:
        existing_user = db.query(model_user).where(model_user.username == person_username.username).first()

        if existing_user is not None:
            existing_person = db.query(model_person).where(model_person.id == existing_user.id_person).first()

            if existing_person is not None:
                existing_person.is_deleted = True
                db.commit()
            else:
                return ReturnMessage(message="Nonexistent person.", code=417)
        else:
            return ReturnMessage(message="Nonexistent user.", code=417)

    except Exception:
        return ReturnMessage(message="Person cannot be updated.", code=417)

    return ReturnMessage(message="Person updated successfully.", code=201)

