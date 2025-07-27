from sqlalchemy.orm import Session
from models.billing_history import BillingHistory
from sqlalchemy_db import get_db


def get_billing_history_by_user_id(user_id: int):
    db = next(get_db())  # ← これが FastAPI のセッション取得パターン
    history = (
        db.query(BillingHistory)
        .filter(BillingHistory.user_id == user_id)
        .order_by(BillingHistory.paid_at.desc())
        .all()
    )
    result = [
        {
            "invoice_id": record.invoice_id,
            "amount": record.amount,
            "currency": record.currency,
            "paid_at": record.paid_at,
        }
        for record in history
    ]
    db.close()
    return result
