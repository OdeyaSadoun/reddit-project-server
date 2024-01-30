from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class changepassword(BaseModel):
    email: str
    old_password: str
    new_password: str