import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean

from api.db.session import Base

class TokenTable(Base):
    __tablename__ = "tokens"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    access_token = Column(String(450), primary_key=True)
    refresh_token = Column(String(450),nullable=False)
    status = Column(Boolean)
    created_date = Column(DateTime, default=datetime.datetime.now)