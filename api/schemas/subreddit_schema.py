from pydantic import BaseModel

from api.enums.reddit_sentiment_enum import ModelRedditSentiment


class SubredditSearchBase(BaseModel):
    reddit_id: int
    title: str
    selftext: str
    sentiment: ModelRedditSentiment
    ups: int
    downs: int
    score: float

class SubredditSearchCreate(SubredditSearchBase):
    pass

class SubredditSearch(SubredditSearchBase):
    id: int

    class Config:
        orm_mode = True
