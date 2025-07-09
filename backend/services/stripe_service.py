# services/stripe_service.py

import stripe
import os

# 環境変数から秘密キーを取得（.envから読み込んでる前提）
stripe.api_key = "REDACTED_STRIPE_TEST_KEY"

print("[DEBUG] Stripe API key is set to:", stripe.api_key)

# 実際にCheckoutセッションを作る処理
def create_checkout_session(email):
    session = stripe.checkout.Session.create(
        mode='subscription',
        customer_email=email,  # ← これがWebhookで取得できるようになる
        line_items=[{
            'price': 'price_1Rfo5eRsRvEmgDyKvpEbkWuj',  # あなたのPrice IDに置き換え
            'quantity': 1,
        }],
        subscription_data={
            'trial_period_days': 30
        },
        success_url='http://localhost:5173/billingsuccess',
        cancel_url='http://localhost:5173/billingcancel',
    )
    return session


