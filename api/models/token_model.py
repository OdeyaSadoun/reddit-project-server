import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean

from api.db.session import Base

class TokenTable(Base):
    __tablename__ = "tokens"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    access_token = Column(String(450), unique=True, nullable=False)
    refresh_token = Column(String(450),nullable=False)
    status = Column(Boolean)
    created_date = Column(DateTime, default=datetime.datetime.now)