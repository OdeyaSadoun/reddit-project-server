import datetime
from sqlalchemy import Column, Integer, String, DateTime
from enum import Enum  # Import the Enum class
from sqlalchemy.dialects.postgresql import ARRAY, ENUM
from api.db.session import Base

class ModelRedditSentiment(str, Enum):
    positive = "positive"
    negative = "negative"
    neutral = "neutral"



class get_posts_by_subreddit_and_categoryedditSearch(Base):
    __tablename__ = 'subredditsearches'
    id = Column(Integer, primary_key=True, index=True)
    reddit_id = Column(Integer, nullable=False)
    title = Column(String(100), nullable=False, index=True)
    selftext = Column(Text, nullable=False, index=True)
    sentiment = Column(ENUM(ModelRedditSentiment), nullable=False, index=True)
    ups = Column(Integer, nullable=False, index=True)
    downs = Column(Integer, nullable=False, index=True)
    score = Column(Float, nullable=False, index=True)
    