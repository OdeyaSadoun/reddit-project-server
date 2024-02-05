import datetime
from sqlalchemy import Column, Integer, String, DateTime
from enum import Enum  # Import the Enum class
from sqlalchemy.dialects.postgresql import ARRAY, ENUM
from api.db.session import Base

class ModelRedditCategory(str, Enum):
    hot = "Hot"
    rising = "Rising"
    top = "Top"
    new = "New"



class RedditSearch(Base):
    __tablename__ = 'redditsearches'
    id = Column(Integer, primary_key=True, index=True)
    reddit = Column(String(100), nullable=False, index=True)
    category = Column(ENUM(ModelRedditCategory), nullable=False, index=True)  # Use ENUM from SQLAlchemy
    search_list = Column(ARRAY(String), nullable=True)