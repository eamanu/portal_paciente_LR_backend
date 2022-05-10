from typing import Optional
from pydantic import BaseModel


class AdminStatus(BaseModel):
    id: Optional[int]
    name: Optional[str]
