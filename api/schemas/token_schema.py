import datetime
from pydantic import BaseModel

class TokenSchemaResponse(BaseModel):
    access_token: str
    refresh_token: str


class TokenSchemaCreate(BaseModel):
    user_id: str
    access_token: str
    refresh_token: str
    status: bool
    created_date: datetime.datetime
