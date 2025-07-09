from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from backend.sqlalchemy_db import Base

class DBUser(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    name = Column(String)
    subscription_status = Column(String, default='none')
    subscription_start = Column(DateTime, default=func.now())
    subscription_end = Column(DateTime, nullable=True)
