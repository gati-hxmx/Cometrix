# stripe_app.py

from flask import Flask, jsonify, request
from flask_cors import CORS
import stripe
import os
from dotenv import load_dotenv
from services.stripe_service import create_checkout_session
from sqlalchemy_db import SessionLocal
from models.user_model import User
from models.subscription_model import Subscription
from datetime import datetime

app = Flask(__name__)
CORS(app, supports_credentials=True, origins=["http://localhost:5173"])

print("[DEBUG] stripe_app.py loaded")

@app.route("/create-checkout-session", methods=["POST"])
def checkout():
    try:
        data = request.get_json()
        email = data.get("email")
        session = create_checkout_session(email)
        return jsonify({"url": session.url})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Stripe設定
load_dotenv()
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
endpoint_secret = os.getenv("STRIPE_WEBHOOK_SECRET")

def stripe_timestamp_to_datetime(ts):
    return datetime.utcfromtimestamp(ts)

@app.route("/webhook", methods=["POST"])
def stripe_webhook():
    payload = request.data
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except stripe.error.SignatureVerificationError:
        return jsonify({"error": "Invalid signature"}), 400

    db = SessionLocal()

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        email = session.get("customer_email")

        if not email:
            return jsonify({"error": "No email in session"}), 400

        user = db.query(User).filter_by(email=email).first()
        if user:
            sub = db.query(Subscription).filter_by(user_id=user.id).first()
            if not sub:
                sub = Subscription(user_id=user.id)
                db.add(sub)

            sub.plan = "pro"
            sub.status = "trialing"
            sub.start_date = stripe_timestamp_to_datetime(session["created"])
            sub.updated_at = datetime.utcnow()
            db.commit()
            print(f"✅ Trial subscription set for {email}")
        else:
            print(f"⚠️ No user found for email: {email}")

    elif event["type"] == "invoice.payment_succeeded":
        invoice      = event["data"]["object"]
        invoice_id   = invoice.get("id")
        customer_id  = invoice.get("customer")
        print(f"[DEBUG] event hit → invoice_id={invoice_id}")

        # ---------- ① まず customer.email を取得 ----------
        try:
            customer = stripe.Customer.retrieve(customer_id)
            email    = customer.get("email")
            print(f"[DEBUG] customer email = {email}")
        except Exception as e:
            print("❌ customer 取得失敗:", e)
            return jsonify({"error": "customer fetch failed"}), 400

        if not email:
            return jsonify({"error": "no email"}), 400

        # ---------- ② user / sub を必ず取得 ----------
        user = db.query(User).filter_by(email=email).first()
        if not user:
            print("⚠️ user 不在 → スキップ")
            return jsonify({"status": "ignored"}), 200

        sub  = db.query(Subscription).filter_by(user_id=user.id).first()
        if not sub:
            print("⚠️ sub 不在 → スキップ")
            return jsonify({"status": "ignored"}), 200

        # ---------- ③ ここから安全に更新 ----------
        sub.status     = "active"
        sub.updated_at = datetime.utcnow()

        try:
            full_invoice = stripe.Invoice.retrieve(invoice_id, expand=["lines"])
            lines = full_invoice["lines"]["data"]
            period_end = lines[0]["period"]["end"] if lines else None
            print(f"[DEBUG] period_end raw = {period_end}")

            if not period_end:
                period_end = invoice.get("current_period_end") or invoice.get("period_end")
                print(f"[DEBUG] fallback period_end = {period_end}")

            if period_end:
                sub.end_date = stripe_timestamp_to_datetime(period_end)
                print(f"[DEBUG] sub.end_date set → {sub.end_date.isoformat()}")
            else:
                print("⚠️ period_end が取得できませんでした")
        except Exception as e:
            import traceback; traceback.print_exc()
            print("⚠️ end_date 設定失敗:", e)

        print(f"[DEBUG] commit 前 end_date = {sub.end_date}")
        db.commit()
        print("✅ invoice.payment_succeeded → DB 更新完了")

        return jsonify({"status": "ok"})
    
    elif event["type"] == "customer.subscription.deleted":
        subscription_obj = event["data"]["object"]
        customer_id = subscription_obj.get("customer")
        canceled_at = subscription_obj.get("canceled_at")  # timestamp
        print(f"[DEBUG] customer.subscription.deleted: customer={customer_id}, canceled_at={canceled_at}")

        try:
            customer = stripe.Customer.retrieve(customer_id)
            email = customer.get("email")
            print(f"[DEBUG] Retrieved customer email: {email}")
        except Exception as e:
            print("❌ Failed to retrieve customer:", e)
            return jsonify({"error": "Failed to retrieve customer"}), 400

        if not email:
            return jsonify({"error": "No email in customer object"}), 400

        user = db.query(User).filter_by(email=email).first()
        if not user:
            print("⚠️ No user found for email:", email)
            return jsonify({"status": "ignored"}), 200

        sub = db.query(Subscription).filter_by(user_id=user.id).first()
        if not sub:
            print("⚠️ No subscription found for user:", email)
            return jsonify({"status": "ignored"}), 200

        sub.status = "canceled"
        if canceled_at:
            sub.end_date = stripe_timestamp_to_datetime(canceled_at)
        sub.updated_at = datetime.utcnow()
        db.commit()

        print(f"✅ Subscription canceled in DB for user: {email}")
        return jsonify({"status": "ok"})



    # ✅ 追加：どのイベントにも一致しない場合のレスポンス
    return jsonify({"status": "ignored"})


@app.route("/cancel-subscription", methods=["POST"])
def cancel_subscription():
    try:
        data = request.get_json()
        email = data.get("email")

        db = SessionLocal()
        user = db.query(User).filter_by(email=email).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        sub = db.query(Subscription).filter_by(user_id=user.id).first()
        if not sub or sub.status not in ["active", "trialing"]:
            return jsonify({"error": "No valid subscription found"}), 400


        # Stripe customer ID を email から取得
        stripe_customers = stripe.Customer.list(email=email).data
        if not stripe_customers:
            return jsonify({"error": "Customer not found in Stripe"}), 404

        stripe_customer_id = stripe_customers[0]["id"]
        stripe_subscriptions = stripe.Subscription.list(customer=stripe_customer_id).data
        if not stripe_subscriptions:
            return jsonify({"error": "No active Stripe subscriptions"}), 404

        stripe_subscription_id = stripe_subscriptions[0]["id"]

        # ✅ Stripe上の subscription を解約予約に変更
        stripe.Subscription.modify(
            stripe_subscription_id,
            cancel_at_period_end=True
        )

        # ✅ 自前DBの status を 'canceling' に更新
        sub.status = "canceling"
        db.commit()

        print(f"📆 解約予約完了: {email}, subscription={stripe_subscription_id}")
        return jsonify({"status": "canceling"}), 200

    except Exception as e:
        import traceback; traceback.print_exc()
        return jsonify({"error": str(e)}), 500



