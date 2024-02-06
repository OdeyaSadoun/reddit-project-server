from sqlalchemy import Column, Integer, String, Text, Double
from sqlalchemy.ext.declarative import declarative_base
class ModelRedditSentiment(str, Enum):
    positive = "positive"
    negative = "negative"
    neutral = "neutral"

class SubredditSearchBase(BaseModel):
    reddit_id: int
    title: str
    selftext: str
    sentiment: ModelRedditSentiment
    ups: int
    downs: int
    score: float

class SubredditSearchCreate(RedditSearchBase):
    pass

class SubredditSearch(RedditSearchBase):
    id: int

    class Config:
        orm_mode = True
