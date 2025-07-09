# backend/models/subscription_model.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy_db import Base

class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    plan = Column(String, nullable=False, default="free")
    status = Column(String, nullable=False, default="active")  # trialing, active, canceled
    start_date = Column(DateTime, server_default=func.now())
    end_date = Column(DateTime)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
