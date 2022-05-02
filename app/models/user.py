import bcrypt
from sqlalchemy import Column, Integer, String

from app.config.database import Base


class User(Base):

    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), nullable=False)
    password = Column(String(500), nullable=False)
    id_person = Column(Integer, nullable=True)
    id_user_status = Column(Integer, nullable=True)
    is_admin = Column(Integer, nullable=False, default=0)
    is_mail_validate = Column(Integer, nullable=True, default=0)

    @staticmethod
    def encrypt_pwd(password):
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode(), salt).decode('utf8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode("utf8"), self.password.encode("utf8"))

    @property
    def admin(self) -> bool:
        return bool(self.is_admin)

    def __init__(
        self, username: str, password: str, id_person: int, id_user_status: int,
        is_admin: bool = False
    ):
        self.username = username
        self.password = self.encrypt_pwd(password)
        self.id_person = id_person
        self.id_user_status = id_user_status
        self.is_admin = is_admin
