from typing import Optional
from pydantic import BaseModel

class patient(BaseModel):
    id: Optional[int]
    name: str
    password: str