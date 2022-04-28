from typing import Optional
from pydantic import BaseModel


class PersonStatus(BaseModel):
    id: Optional[int]
    name: Optional[str]
