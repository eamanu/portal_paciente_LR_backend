from sqlalchemy.orm import Session
from app.model import Users


def login(db: Session, user_id: str, password: str) -> bool:
    user = db.query(Users).filter_by(user_id=user_id).first()  # type: Users
    if user is None:
        return False
    return user.check_password(password)
