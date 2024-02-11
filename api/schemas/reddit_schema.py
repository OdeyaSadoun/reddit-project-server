import datetime
from pydantic import BaseModel
from typing import List
from enum import Enum  # Import the Enum class


class ModelRedditCategory(str, Enum):
    hot = "hot"
    rising = "rising"
    top = "top"
    new = "new"



class RedditSearchBase(BaseModel):
    user_id: int
    reddit: str
    category: ModelRedditCategory
    created_date: datetime.datetime


class RedditSearchCreate(RedditSearchBase):
    pass

class RedditSearch(RedditSearchBase):
    id: int

    class Config:
        orm_mode = True
