from pydantic import BaseModel

class requestdetails(BaseModel):
    email: str
    password: str