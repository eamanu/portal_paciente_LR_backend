from pydantic import BaseModel


class ResponseOK(BaseModel):
    message: str
    code: int
    status: bool = True


class ResponseNOK(BaseModel):
    message: str
    code: int
    status: bool = False
