from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy_db import Base
from datetime import datetime


class BillingHistory(Base):
    __tablename__ = "billing_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    invoice_id = Column(String, nullable=True)
    amount = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(10), default="jpy")
    paid_at = Column(DateTime, default=func.now())
    billing_date = Column(DateTime)
    period_start = Column(DateTime, nullable=True)
    period_end = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # 任意：逆参照が必要な場合のみ
    user = relationship("User", backref="billing_history")
