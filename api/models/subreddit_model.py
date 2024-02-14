import datetime
from sqlalchemy import Column, Integer, String, Text, Float
from sqlalchemy.dialects.postgresql import ENUM
from api.db.session import Base
from sqlalchemy.orm import validates

from api.enums.reddit_sentiment_enum import ModelRedditSentiment


class SubredditSearch(Base):
    __tablename__ = 'subredditsearches'
    id = Column(Integer, primary_key=True, index=True)
    reddit_id = Column(Integer, nullable=False)
    title = Column(String(1000), nullable=False, index=True)
    selftext = Column(Text, nullable=False, index=True)
    sentiment = Column(ENUM(ModelRedditSentiment), nullable=False, index=True)
    ups = Column(Integer, nullable=False, index=True)
    downs = Column(Integer, nullable=False, index=True)
    score = Column(Float, nullable=False, index=True)

    @validates('selftext')
    def validate_selftext(self, key, value):
        if len(value) > 2000:
            value = value[:2000] 
        return value