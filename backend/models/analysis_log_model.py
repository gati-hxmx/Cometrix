# backend/models/analysis_log_model.py

from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy_db import Base

class AnalysisLog(Base):
    __tablename__ = "analysis_logs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    video_url = Column(Text, nullable=False)
    video_title = Column(Text)
    platform = Column(String, nullable=False)  # "youtube" or "twitch"
    analyzed_at = Column(DateTime, server_default=func.now())
    comment_count = Column(Integer)
    duration_sec = Column(Integer)
    result_path = Column(Text)
