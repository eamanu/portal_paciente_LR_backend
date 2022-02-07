import bcrypt
from sqlalchemy import Column, Integer, String

from app.config.database import Base


class User(Base):

    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), nullable=False)
    password = Column(String(500), nullable=False)
    id_person = Column(Integer, nullable=False)
    id_user_status = Column(Integer, nullable=False)

    '''
    @property
    def password(self):
        raise AttributeError("password: write-only field")


    @password.setter
    def password(self, password):
        salt = bcrypt.gensalt()
        self.password = bcrypt.hashpw(password.encode('utf8'), salt)
    '''

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf8'), self.password.encode('utf8'))
