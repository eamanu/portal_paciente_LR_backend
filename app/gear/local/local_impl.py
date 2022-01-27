from app.models.user import User as model_user
from app.schemas.user import User as schema_user
from sqlalchemy.orm import Session
from app.config.database import SessionLocal

class Local_Impl:

    def __init__(self):
        pass

    db: Session = SessionLocal()

    def get_users(self):
        value = self.db.query(model_user).fetchall()
        return value


    def create_user(self, user: schema_user):

        new_user = model_user()

        new_user.username = user.username
        new_user.password = user.password
        new_user.id_person = user.id_person
        new_user.id_user_status = user.id_user_status

        self.db.add(new_user)
        self.db.commit()
        value = self.db.query(model_user).where(model_user.id == new_user.id).first()
        return value


    def get_user(self, id: int):
        value = self.db.query(model_user).where(model_user.id == id).first()
        return value

    def get_user(self, username: str):
        value = self.db.query(model_user).where(model_user.username == username).first()
        return value

    def delete_user(self, id: str):

        old_user = model_user()

        old_user = self.db.query(model_user).where(model_user.id == id).first()
        self.db.delete(old_user)
        self.db.commit()
        return old_user


