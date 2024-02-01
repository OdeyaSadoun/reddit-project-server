from pydantic import BaseModel


class ChangePasswordSchema(BaseModel):
    email: str
    old_password: str
    new_password: str


class LoginSchema(BaseModel):
    email: str
    password: str
