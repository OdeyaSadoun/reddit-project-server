from pydantic import BaseModel
from typing import List
from enum import Enum  # Import the Enum class


class ModelRedditCategory(str, Enum):
    hot = "Hot"
    rising = "Rising"
    top = "Top"
    new = "New"



class RedditSearchBase(BaseModel):
    user_id: int
    reddit: str
    category: ModelRedditCategory
    search_list: List[str]

class RedditSearchCreate(RedditSearchBase):
    pass

class RedditSearch(RedditSearchBase):
    id: int

    class Config:
        orm_mode = True
