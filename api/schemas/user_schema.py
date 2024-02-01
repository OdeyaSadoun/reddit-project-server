import datetime
from pydantic import BaseModel


class UserSchemaCreate(BaseModel):
    name: str
    email: str
    password: str


class UserSchemaResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True
