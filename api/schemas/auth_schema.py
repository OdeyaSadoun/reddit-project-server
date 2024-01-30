from pydantic import BaseModel
import datetime

class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class TokenCreate(BaseModel):
    user_id: str
    access_token: str
    refresh_token: str
    status: bool
    created_date: datetime.datetime


class changepassword(BaseModel):
    email: str
    old_password: str
    new_password: str