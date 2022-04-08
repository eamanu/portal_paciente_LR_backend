import re

from sqlalchemy import Column, Integer, String

from app.config.config import DEBUG_ENABLED
from app.config.database import Base
from app.config.database import SessionLocal
from app.models.role_permission import RolePermission
from app.models.user import User
from app.models.user_role import UserRole



class Permission(Base):

    __tablename__ = "permission"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    url = Column(String(1000), nullable=False)
    method = Column(String(10), nullable=False)

    @staticmethod
    def user_is_authorized(username: str, path: str, method: str) -> bool:
        db = SessionLocal()
        debug = False

        permissions = db.query(Permission) \
            .join(RolePermission, RolePermission.id == RolePermission.id_permission) \
            .join(UserRole, RolePermission.id_role == UserRole.id_role) \
            .join(User, UserRole.id_user == User.id and User.username == username) \
            .all()

        for permission in permissions:
            patterns = [permission.url]
            pattern = '(?:% s)' % '|'.join(patterns)
            if re.match(pattern, path) and permission.method.upper() == method.upper():

                if DEBUG_ENABLED:
                    print("---------------------------")
                    print(permission.name)
                    print(permission.url)
                    print(path)
                    print(permission.method)
                    print(method)
                    print("---------------------------")

                return True

        return False
