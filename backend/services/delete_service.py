import os
from sqlalchemy.orm import Session
from models import User, Subscription, AnalysisLog, BillingHistory
from services.stripe_service import cancel_subscription_by_customer_id


import stripe

def delete_user_account(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise Exception("ユーザーが見つかりません")

    # ✅ Stripe customer ID を email から取得
    stripe_customers = stripe.Customer.list(email=user.email).data
    if stripe_customers:
        stripe_customer_id = stripe_customers[0]["id"]
        subscriptions = stripe.Subscription.list(customer=stripe_customer_id).data
        for sub in subscriptions:
            stripe.Subscription.delete(sub["id"])  # 即時解約
        print(f"🗑️ Stripe上のsubscriptionを削除しました: {user.email}")
    else:
        print(f"⚠️ Stripe Customerが見つかりません: {user.email}")

    # ✅ 自前DBから関連データを削除
    db.query(Subscription).filter_by(user_id=user.id).delete()
    db.query(AnalysisLog).filter_by(user_id=user.id).delete()
    db.query(BillingHistory).filter_by(user_id=user.id).delete()
    db.delete(user)
    db.commit()
    print(f"✅ ユーザーと関連データを削除しました: {user.email}")



