# services/stripe_service.py

import stripe
import os

# 環境変数から秘密キーを取得（.envから読み込んでる前提）
stripe.api_key = "REDACTED_STRIPE_TEST_KEY"

print("[DEBUG] Stripe API key is set to:", stripe.api_key)

# 実際にCheckoutセッションを作る処理
def create_checkout_session():
    return stripe.checkout.Session.create(
        mode="subscription",
        payment_method_types=["card"],
        line_items=[{
            "price": "price_1Rfo5eRsRvEmgDyKvpEbkWuj",  # あなたの Price ID に置き換え！
            "quantity": 1,
        }],
        success_url="http://localhost:5173/mypage?success=true",
        cancel_url="http://localhost:5173/mypage?canceled=true",
    )
