import bcrypt
from sqlalchemy import Column, Integer, String

from app.database import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(25), nullable=False)
    password_hash = Column(String(100), nullable=False)

    @property
    def password(self):
        raise AttributeError("password: write-only field")

    @password.setter
    def password(self, password):
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode('utf8'), salt)

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf8'), self.password_hash.encode('utf8'))
