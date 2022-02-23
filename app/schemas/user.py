from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    # id: Optional[int]
    username: Optional[str]
    password: Optional[str]
    id_person: Optional[int]
    id_user_status: Optional[int]
