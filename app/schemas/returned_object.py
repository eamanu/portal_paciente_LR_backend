from pydantic import BaseModel


class ReturnMessage(BaseModel):
    message: str
    code: int
