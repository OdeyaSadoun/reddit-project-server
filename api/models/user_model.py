import datetime
from sqlalchemy import Column, Integer, String, DateTime

from api.db.session import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password = Column(String(100), nullable=False)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
