from typing import Optional
from pydantic import BaseModel


class Category(BaseModel):
    id: Optional[int]
    name: Optional[str]
