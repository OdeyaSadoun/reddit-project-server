import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, Float
from enum import Enum
from sqlalchemy.dialects.postgresql import ARRAY, ENUM
from api.db.session import Base
from sqlalchemy.orm import validates

class ModelRedditSentiment(str, Enum):
    positive = "positive"
    negative = "negative"
    neutral = "neutral"

class SubredditSearch(Base):
    __tablename__ = 'subredditsearches'
    id = Column(Integer, primary_key=True, index=True)
    reddit_id = Column(Integer, nullable=False)
    title = Column(String(100), nullable=False, index=True)
    selftext = Column(Text, nullable=False, index=True)
    sentiment = Column(ENUM(ModelRedditSentiment), nullable=False, index=True)
    ups = Column(Integer, nullable=False, index=True)
    downs = Column(Integer, nullable=False, index=True)
    score = Column(Float, nullable=False, index=True)

    @validates('selftext')
    def validate_selftext(self, key, value):
        if len(value) > 2000:
            value = value[:2000]  # חיתוך המחרוזת לאורך מקסימלי של 6000 תווים
        return value