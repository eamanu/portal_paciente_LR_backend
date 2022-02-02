from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class ExpirationBackList(BaseModel):
    id: Optional[int]
    register_datetime: Optional[datetime]
    token: Optional[str]
