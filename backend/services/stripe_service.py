# services/stripe_service.py

import os
import stripe
from dotenv import load_dotenv

load_dotenv()
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
print("[DEBUG] Stripe API key is set:", bool(stripe.api_key))

# ✅ Checkout セッションを作成
def create_checkout_session(email):
    session = stripe.checkout.Session.create(
        mode='subscription',
        customer_email=email,
        line_items=[{
            'price': 'price_1Rfo5eRsRvEmgDyKvpEbkWuj',  # 本番環境では.envから取得でもOK
            'quantity': 1,
        }],
        subscription_data={
            'trial_period_days': 30
        },
        success_url='http://localhost:5173/billingsuccess',
        cancel_url='http://localhost:5173/billingcancel',
    )
    return session

# ✅ 顧客IDから全サブスクリプションをキャンセル
def cancel_subscription_by_customer_id(customer_id):
    try:
        subs = stripe.Subscription.list(customer=customer_id)
        for sub in subs.auto_paging_iter():
            stripe.Subscription.delete(sub.id)
            print(f"✅ Stripe上のサブスクリプション {sub.id} をキャンセルしました")
        return True
    except Exception as e:
        print(f"🟥 Stripeサブスクリプションのキャンセルに失敗: {e}")
        return False

# ✅ email を元に即時キャンセル（主に FastAPI 側で使用）
def cancel_stripe_subscription_immediately(email: str) -> bool:
    try:
        customers = stripe.Customer.list(email=email).data
        if not customers:
            raise Exception("Stripe customer not found")

        customer_id = customers[0]["id"]

        subscriptions = stripe.Subscription.list(customer=customer_id, status="all").data
        if not subscriptions:
            raise Exception("No subscriptions found for this customer")

        stripe.Subscription.delete(subscriptions[0]["id"])
        print(f"✅ Stripe subscription immediately canceled for {email}")
        return True
    except Exception as e:
        print("🟥 Stripeキャンセル失敗:", e)
        raise
