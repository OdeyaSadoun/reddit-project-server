import datetime
from sqlalchemy import Column, Integer, String, DateTime
from enum import Enum  # Import the Enum class
from sqlalchemy.dialects.postgresql import ARRAY, ENUM
from api.db.session import Base

class ModelRedditCategory(str, Enum):
    hot = "hot"
    rising = "rising"
    top = "top"
    new = "new"


class RedditSearch(Base):
    __tablename__ = 'redditsearches'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    reddit = Column(String(100), nullable=False, index=True)
    category = Column(ENUM(ModelRedditCategory), nullable=False, index=True)  # Use ENUM from SQLAlchemy
