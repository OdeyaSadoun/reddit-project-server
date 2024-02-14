import datetime
from pydantic import BaseModel

from api.enums.reddit_category_enum import ModelRedditCategory


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
