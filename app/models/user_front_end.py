import bcrypt
from sqlalchemy import Column, Integer, String

from app.config.database import Base

class UserFrontEnd(Base):
    __tablename__ = "user0"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), nullable=False)
    password_hash = Column(String(500), nullable=False)
    id_person = Column(Integer, nullable=False)
    id_user_status = Column(Integer, nullable=False)

    @property
    def password(self):
        raise AttributeError("password: write-only field")

    @password.setter
    def password(self, password):
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode('utf8'), salt)
        print(self.password_hash)

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf8'), self.password_hash.encode('utf8'))
