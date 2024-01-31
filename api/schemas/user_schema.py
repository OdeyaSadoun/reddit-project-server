import datetime
from pydantic import BaseModel

class UserSchemaCreate(BaseModel):
    username: str
    email: str
    password: str
    created_date: datetime.datetime


class UserSchemaResponse(BaseModel):
    id: int
    username: str
    email: str
    
    class Config:
        orm_mode = True    


