import datetime
from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    created_date: datetime.datetime


class UserSchema(BaseModel):
    id: int
    username: str
    email: str
    password: str


