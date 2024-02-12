import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import ENUM
from api.db.session import Base
from api.enums.reddit_category_enum import ModelRedditCategory


class RedditSearch(Base):
    __tablename__ = 'redditsearches'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    reddit = Column(String(100), nullable=False, index=True)
    category = Column(ENUM(ModelRedditCategory), nullable=False, index=True)
    created_date = Column(DateTime, default=datetime.datetime.now)

