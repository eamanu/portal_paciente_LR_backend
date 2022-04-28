from pydantic import BaseModel


class ResponseOK(BaseModel):
    value: str = ""
    message: str
    code: int
    status: bool = True


class ResponseNOK(BaseModel):
    value: str = ""
    message: str
    code: int
    status: bool = False


class HTTPError(BaseModel):
    detail: str

    class Config:
        schema_extra = {
            "example": {"detail": "HTTPException raised."},
        }
