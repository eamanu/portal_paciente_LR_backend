from pydantic import BaseModel


class AccessToken(BaseModel):
    access_token: str

    class Config:
        orm_mode = True
