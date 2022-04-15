from typing import Optional
from pydantic import BaseModel
from pydantic_sqlalchemy import sqlalchemy_to_pydantic
from app.models.message import Message as model_message


Message = sqlalchemy_to_pydantic(model_message)


class ReadMessage(BaseModel):
    message: Message
    read_datetime: Optional[str]
